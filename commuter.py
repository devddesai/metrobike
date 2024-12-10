#imports
from mesa import Agent
import pathfinding as pf

class Commuter(Agent):

    def __init__(self, model, current_pos, distance_left, intermediate_node, destination):
        """
        Initializes a commuter agent with a current position, distance left to the intermediate node, the intermediate node, and the destination.
        The agent also has a stopwatch to measure time spent on a trip, a boolean to indicate whether the agent is biking, and a list of lists to 
        store the time needed to walk directly to the destination, and the time actually spent walking/biking.
        The agent also has a counter for the number of trips taken, and a counter for the number of times the agent has failed to park a bike.

        Args:
        ---
        model: Model
            The model the agent is in
        current_pos: int
            The agent's current position
        distance_left: int
            The distance left to the intermediate node, in terms of time
        intermediate_node: int
            The agent's intermediate node needed to reach the destination, if intermediate node is a the destination, the trip will end once
            the agent reaches the destination
        destination: int
            The agent's destination
        """
        super().__init__(model)
        self.destination = destination # The agent's destination
        self.intermediate_node = intermediate_node # The agent's intermediate node needed to reach the destination
        self.distance_left = distance_left # The distance left to the intermediate node, in terms of time
        self.current_pos = current_pos # The agent's current position
        self.biking = False # Whether the agent is currently biking
        self.stopwatch = 0 # The agent's stopwatch, used to measure time spent completing a trip
        self.walking_watch = 0
        self.num_trips = 0
        self.walking_time = pf.walk_cost(self.model.grid.G, self.current_pos, self.destination, walk_multiplier=self.model.walking_multiplier) # The time it takes to walk to the destination directly from the initial destination
        self.time_saved = [[self.walking_time]] # List of lists, where each list contains the time needed to walk directly, and time actually spent walking/biking
        self.park_failures = 0 # Number of times the agent has failed to park a bike bc no spots were available

        assert self.model.grid.G.nodes[self.current_pos]['type'] == 'destination', "Agent must start at a destination"
        
    def step(self):
        """
        The agent's step function, which updates the agent's position, stopwatch, and other attributes for the current trip.
        The agent will move to the intermediate node, and if the agent has reached the intermediate node, the agent will set 
        a new start node according to the pathfinding algorithm. If the agent has reached the destination, the agent will set 
        a new destination

        Updates the agent's position, stopwatch, and other attributes for the agent as needed.

        Args:
        ---
        None

        Returns:
        ---
        None
        """
        # update the agent's position and stopwatch for current trip
        self.current_pos = self.model.get_node(self)
        self.stopwatch += 1
        if self.biking:
            self.walking_watch += 1

        # If the agent has reached the intermediate node, set new start node
        if self.distance_left <= 0:
            # If the agent has reached the intermediate node, set new start node
            self.current_pos = self.intermediate_node
            self.model.grid.move_agent(self, self.current_pos)
            
            if self.model.grid.G.nodes[self.current_pos]['type'] == 'station':
                self.model.grid.G.nodes[self.current_pos]['data'].popularity += 1

            # Return bike if the agent is at the intended station and there are spots available
            # if self.biking and self.model.grid.G.nodes[self.current_pos]['type'] == 'station' and self.model.grid.G.nodes[self.current_pos]['data'].get_spot_availability():
            #     self.model.grid.G.nodes[self.current_pos]['data'].return_bike()
            #     self.biking = False

            # If the agent has reached the destination, set new destination
            # Else, the agent will rent a bike if it is at a station and there are bikes available
            if self.current_pos == self.destination:
                self.time_saved[-1].append(self.stopwatch)
                self.stopwatch = 0
                self.destination = self.model.sample_destination(self.current_pos)
                self.walking_time = pf.walk_cost(self.model.grid.G, self.current_pos, self.destination, walk_multiplier=self.model.walking_multiplier)
                self.time_saved.append([self.walking_time])
                self.num_trips += 1
            elif not(self.biking) and self.model.grid.G.nodes[self.current_pos]['type'] == 'station' and self.model.grid.G.nodes[self.current_pos]['data'].get_bike_availability():
                # self.model.grid.G.nodes[self.current_pos]['data'].rent_bike()
                # self.biking = True
                pass

            #### commented this out, Dev's implementation of parking failures changed this and is below
            # elif self.biking and self.model.grid.G.nodes[self.current_pos]['type'] == 'station' and self.model.grid.G.nodes[self.current_pos]['data'].get_spot_availability():
            #     self.model.grid.G.nodes[self.current_pos]['data'].return_bike()
            #     self.biking = False

            ### testing park failures
            elif self.biking and self.model.grid.G.nodes[self.current_pos]['type'] == 'station':
                if self.model.grid.G.nodes[self.current_pos]['data'].get_spot_availability():
                    self.model.grid.G.nodes[self.current_pos]['data'].return_bike()
                    self.biking = False
                else:
                    self.park_failures += 1

            # Set new intermediate node
            if self.model.grid.G.nodes[self.current_pos]['type'] == 'destination':
                path = pf.pathfind(self.model.grid.G, self.current_pos, self.destination, False, walk_multiplier=self.model.walking_multiplier)
            else:
                bike = self.model.grid.G.nodes[self.current_pos]['data'].get_bike_availability()
                path = pf.pathfind(self.model.grid.G, self.current_pos, self.destination, bike, walk_multiplier=self.model.walking_multiplier)
                if not(path[1]) and self.biking:
                    path = pf.bike_std(self.model.grid.G, self.current_pos, self.destination)

            self.intermediate_node = path[0]
            
            if path[1]:
                self.distance_left = self.model.grid.G[self.current_pos][self.intermediate_node]['weight']
                if not(self.biking):
                    self.model.grid.G.nodes[self.current_pos]['data'].rent_bike()
                    self.biking = True
            else:
                self.distance_left = self.model.grid.G[self.current_pos][self.intermediate_node]['weight'] * self.model.walking_multiplier
        else:
            self.distance_left -= 1        

    
    def get_agent_position(self):
        """
        Returns the agent's current position

        Args:
        ---
        None

        Returns:
        ---
        int: The agent's current position
        """
        return self.current_pos
    
    def get_distance_left(self):
        """
        Returns the distance left to the intermediate node

        Args:
        ---
        None

        Returns:
        ---
        int: The distance left to the intermediate node
        """
        return self.distance_left
    
    def get_agent_destination(self):
        """
        Returns the agent's destination

        Args:
        ---
        None

        Returns:
        ---
        int: The agent's destination
        """
        return self.destination
    
    def get_intermediate_node(self):
        """
        Returns the agent's intermediate node

        Args:
        ---
        None

        Returns:
        ---
        int: The agent's intermediate node
        """
        return self.intermediate_node
    
    def get_stopwatch(self):
        """
        Returns the agent's stopwatch

        Args:
        ---
        None

        Returns:
        ---
        int: The agent's stopwatch
        """
        return self.stopwatch
    
    def get_station_info(self):
        """
        Returns the number of bikes available at the agent's current position if the agent is at a station, otherwise returns "at dest"

        Args:
        ---
        None

        Returns:
        ---
        int or str: The number of bikes available at the agent's current position if the agent is at a station, otherwise "at dest"
        """
        if self.model.grid.G.nodes[self.current_pos]['type'] == 'station':
            return self.model.grid.G.nodes[self.current_pos]['data'].available_bikes
        else:
            return "at dest"
    
    def get_next_station_info(self):
        """
        Returns the number of bikes available at the agent's intermediate node if the agent's intermediate node is a station, otherwise returns "no intermed"

        Args:
        ---
        None

        Returns:
        ---
        int or str: The number of bikes available at the agent's intermediate node if the agent's intermediate node is a station, otherwise "no intermed"
        """
        if self.model.grid.G.nodes[self.intermediate_node]['type'] == 'station':
            return self.model.grid.G.nodes[self.intermediate_node]['data'].available_bikes
        else:
            return "no intermed"
    
    def get_all_station_info(self):
        """
        Returns a dictionary of all stations and the number of bikes available at each station

        Args:
        ---
        None

        Returns:
        ---
        dict: A dictionary of all stations and the number of bikes available at each station
        """
        dic = {}
        for station in self.model.stations:
            dic[station] = self.model.grid.G.nodes[station]['data'].available_bikes
        return dic

    def bike_boolean(self):
        """
        Returns whether the agent is currently biking

        Args:
        ---
        None

        Returns:
        ---
        bool: Whether the agent is currently biking
        """
        return self.biking
    
    def park_failure(self):
        """
        Returns the number of times the agent has failed to park a bike

        Args:
        ---
        None

        Returns:
        ---
        int: The number of times the agent has failed to park a bike
        """
        return self.park_failures

    def get_num_trips(self):
        """
        Returns the number of trips the agent has taken

        Args:
        ---
        None

        Returns:
        ---
        int: The number of trips the agent has taken
        """
        return self.num_trips