#imports
from mesa import Model
from mesa.space import NetworkGrid
from mesa.datacollection import DataCollector
import network_example as ne
import numpy as np
import pathfinding as pf
import commuter as cm


class MyModel(Model):
    def __init__(self, n_agents, seed=None, G=ne.basic_graph()[0], destination_pos=ne.basic_graph()[1][4:], weights = ne.basic_weights(), bike_init=None):
        """
        Create a new model with the given number of agents and seed
        
        Parameters
        ----------
        n_agents : int
            The number of agents to be created
        seed : int
            The seed to be used for random number generation
        G : nx.Graph
            The graph to be used for the model
        destination_pos : list
            The list of destination node indices
        weights : list
            The list of weights for sampling destinations
        bike_init : dict
            The dictionary of initial bike counts for each station
        """

        # Initialize the model, set up random seeds for mesa and numpy
        super().__init__(seed=seed)
        self.rng = np.random.default_rng(seed)

        # graph initialization and time multiplier for walking
        g = G
        self.walking_multiplier = 3
        self.grid = NetworkGrid(g)

        # storing all stations and destination node indices
        self.stations = pf.get_stations(self.grid.G)
        self.destinations = pf.get_destinations(self.grid.G)
        self.destination_pos = destination_pos

        if bike_init is not None:
            self.assign_bikes(bike_init)
        
        # data collector
        """
        self.datacollector = DataCollector(
            agent_reporters={"Position": lambda agent: agent.get_agent_position(),
                             "Distance_Left": lambda agent: agent.get_distance_left(),
                             "Intermediate_Node": lambda agent: agent.get_intermediate_node(),
                             "Destination": lambda agent: agent.get_agent_destination(),
                             "Stopwatch": lambda agent: agent.get_stopwatch(),
                            #  "Cur Station Capacity": lambda agent: agent.get_station_info(),
                            #  "Next Station Capacity": lambda agent: agent.get_next_station_info(),
                             "All Station Capacity": lambda agent: agent.get_all_station_info(),
                             "Biking": lambda agent: agent.bike_boolean(),
                             "Park Failures": lambda agent: agent.park_failure(),
                             "Trips": lambda agent: agent.num_trips
                             })
        """

        # destination weights for sampling
        self.destination_w = weights

        # Create agents and place them on the grid
        for i in range(1, n_agents + 1):
            node_id = self.random.choice(self.destinations)
            destination_node = self.sample_destination(node_id)
            # print(node_id, destination_node)
            path = pf.pathfind(self.grid.G, node_id, destination_node, False, walk_multiplier=self.walking_multiplier)
            intermediate_node = path[0]
            distance_left = self.grid.G[node_id][intermediate_node]['weight'] * self.walking_multiplier

            commuter = cm.Commuter(self, current_pos=node_id, distance_left=distance_left, intermediate_node=intermediate_node, destination=destination_node)

            self.grid.place_agent(commuter, node_id)
            
        # self.datacollector.collect(self)
    
    def get_node(self, agent):
        """
        Returns the node ID of the given agent if it is found in the grid

        Parameters
        ----------
        agent : Agent
            The agent whose node ID is to be found

        Returns
        -------
        node_id : int
            The node ID of the given agent
        """
        # Iterate over all node IDs in the graph
        for node_id in self.grid.G.nodes():
            # Get the agents at the current node
            agents_at_node = self.grid.get_cell_list_contents([node_id])
            # If the given agent is found at this node, return the node ID
            if agent in agents_at_node:
                return node_id
        return None  # If the agent is not found in any node

    def sample_destination(self, current_pos):
        """
        Sample a destination for an agent to travel to

        Parameters
        ----------
        current_pos : int
            The current position index of the agent
        
        Returns
        -------
        destination: int
            The destination node index
        """
        while True:
            destination = self.rng.choice(self.destinations, p=self.destination_w)
            if destination != current_pos:
                return destination
            
    def assign_bikes(self, bike_counts):
        """
            For each station, assign a number of bikes to the station

            Parameters
            ----------
            bike_counts : dict
                A dictionary where the keys are station indices and the values are the number of bikes to be assigned to the station

            Returns
            -------
            None
        """
        for station in self.stations:
            assert station in bike_counts, "All stations must be assigned a number of bikes"
            self.grid.G.nodes[station]['data'].assign_bikes(bike_counts[station])

    def set_station_data(self, capacity, available_bikes):
        """
            Set the capacity and available bikes for each station

            Parameters
            ----------
            capacity : dict
                A dictionary where the keys are station indices and the values are the capacity of the station
            available_bikes : dict
                A dictionary where the keys are station indices and the values are the number of available bikes at the station

            Returns
            -------
            None
        """
        for station in self.stations:
            self.grid.G.nodes[station]['data'].set_station_info(capacity, available_bikes)


    def step(self):
        self.agents.shuffle_do("step")
        # self.datacollector.collect(self)
    
    def time_saved_ratio(self):
        """
            The ratio of time traveled with biking & walking to time traveled with only walking

            Parameters
            ----------
            agent : Agent
                The agent whose time saved is inputted

            Returns
            -------
            ratio : float
                The ratio of time traveled with biking & walking to time traveled with only walking
        """
        totalwalk=0
        realtime=0
        for agent in self.agents:
            time = agent.time_saved
            for x in time:
                if len(x) == 2:
                    totalwalk += x[0]
                    realtime += x[1]
        return totalwalk, realtime, realtime/totalwalk
    
    def trips_average(self):
        avg = 0
        for agent in self.agents:
            avg += agent.get_num_trips()
        return avg/len(self.agents)