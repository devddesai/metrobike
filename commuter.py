#imports


class Commuter(Agent):

    def __init__(self, model, current_pos, distance_left, intermediate_node, destination):
        super().__init__(model)
        self.destination = destination # The agent's destination
        self.intermediate_node = intermediate_node # The agent's intermediate node needed to reach the destination
        self.distance_left = distance_left # The distance left to the intermediate node, in terms of time
        self.current_pos = current_pos # The agent's current position
        self.biking = False # Whether the agent is currently biking
        self.stopwatch = 0 # The agent's stopwatch, used to measure time spent completing a trip
        self.walking_time = pf.walk_cost(self.model.grid.G, self.current_pos, self.destination, walk_multiplier=self.model.walking_multiplier) # The time it takes to walk to the destination directly from the initial destination
        self.time_saved = [[self.walking_time]] # List of lists, where each list contains the time needed to walk directly, and time actually spent walking/biking
        self.park_failures = 0 # Number of times the agent has failed to park a bike bc no spots were available

        assert self.model.grid.G.nodes[self.current_pos]['type'] == 'destination', "Agent must start at a destination"
        
    def step(self):
        # update the agent's position and stopwatch for current trip
        self.current_pos = self.model.get_node(self)
        self.stopwatch += 1

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
        return self.current_pos
    
    def get_distance_left(self):
        return self.distance_left
    
    def get_agent_destination(self):
        return self.destination
    
    def get_intermediate_node(self):
        return self.intermediate_node
    
    def get_stopwatch(self):
        return self.stopwatch
    
    def get_station_info(self):
        if self.model.grid.G.nodes[self.current_pos]['type'] == 'station':
            return self.model.grid.G.nodes[self.current_pos]['data'].available_bikes
        else:
            return "at dest"
    
    def get_next_station_info(self):
        if self.model.grid.G.nodes[self.intermediate_node]['type'] == 'station':
            return self.model.grid.G.nodes[self.intermediate_node]['data'].available_bikes
        else:
            return "no intermed"
    
    def get_all_station_info(self):
        numword = {0: 'zero', 1: 'one', 2: 'two', 3: 'three', 4: 'four'}
        return [str(station) + ":" +str({self.model.grid.G.nodes[station]['data'].available_bikes}) for station in self.model.stations]

    def bike_boolean(self):
        return self.biking
    
    def park_failure(self):
        return self.park_failures