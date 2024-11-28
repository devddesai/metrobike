import numpy as np

class SimulatedAnnealer():
    """
    Simulated Annealing algorithm for optimization problems.

    Attributes:
        current_state (list[tuple]) : The current state of the system, represented as the positions of the stations in a grid.
        cost_function (function) : The cost function to be minimized.
        temperature (float) : The initial temperature of the system.
        iter (int) : The number of iterations at each temperature.
        alpha (float) : The cooling rate of the system.
        
    """

    def __init__ (self, initial_state, cost_function, temperature, iter, alpha):
        self.current_state, self.cost_function = self.unpacker(initial_state, cost_function(initial_state))
        self.temperature = temperature
        self.best_state = self.current_state
        self.best_cost = self.cost_function(self.current_state)
        self.current_cost = self.best_cost
        self.iter = iter
        self.alpha = alpha

    def unpacker(self, state, cost):
        # NYI - Formats the initial_state and cost_function output to be compatible with the simulated annealing algorithm
        return state, cost    
    
    def eval(self):
        return self.cost_function(self.current_state)
    
    def neighbor(self, num):
        assert num <= len(self.current_state), "Number of stations to move must be less than or equal to the number of stations in the grid"
        new_state = self.current_state.copy()
        random_stations = np.random.choice(self.current_state, num, replace=False)
        for station in random_stations:
            new_station = self.move(station)
            new_state.remove(station)
            new_state.append(new_station)
        return new_state

    def move(self, station):
        moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        move = np.random.choice(moves)
        moves.remove(move)
        new_station = station[0] + move[0], station[1] + move[1]
        while (new_station in self.current_state or not self.valid(new_station)) and moves:
            move = np.random.choice(moves)
            moves.remove(move)
            new_station = station[0] + move[0], station[1] + move[1]
        if not moves:
            return station
        return new_station
    
    def valid(self, station):
        # NYI - Checks if the station is within the grid
        return True
    
    def anneal(self, threshold, num):
        while self.temperature > threshold:
            for _ in range(self.iter):
                new_state = self.neighbor(num)
                new_cost = self.cost_function(new_state)
                if new_cost < self.current_cost:
                    self.current_cost = new_cost
                    self.current_state = new_state
                    if new_cost < self.best_cost:
                        self.best_cost = new_cost
                        self.best_state = self.current_state
                elif np.random.rand() < np.exp((self.current_cost - new_cost) / self.temperature):
                    self.current_cost = new_cost
                    self.current_state = new_state
            self.temperature *= self.alpha
        return self.best_state, self.best_cost
