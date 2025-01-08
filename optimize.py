import numpy as np
from tqdm.notebook import tqdm
import matplotlib.pyplot as plt

class Optimize():
    """
    Particle Swarm Optimization
    
    Attributes
    ---
    minval (float) : The minimum value of the search space.
    maxval (float) : The maximum value of the search space.
    fitness (function) : The fitness function to be optimized.
    w (float) : The inertia weight.
    c1 (float) : The cognitive parameter.
    c2 (float) : The social parameter.
    """
    
    def __init__(self, citymap, fitness, w, c1, c2, stations=[]):
        """
        Parameters
        ---
        citymap (list) : A list of coordinates (tuples). The first two should be the minimum and maximum corners of the search space.
                            The rest should be coordinates of the destination nodes.
        fitness (function) : The fitness function to be optimized. The function should take a dictionary of coordinates with the key being the type of node
                                and value being a list of the coordinates of the nodes, and return a float (time saved)
        w (float) : The inertia weight.
        c1 (float) : The cognitive parameter.
        c2 (float) : The social parameter.
        stations (list) : A list of coordinates (tuples) of fixed stations (won't be optimized)
        
        Attributes
        ---
        xwidth (float) : The width of the search space.
        ywidth (float) : The height of the search space.
        center (tuple) : The center of the search space.
        fitness (function) : The fitness function to be optimized. The function should take a list of coordinates and return a float (time saved)
        w (float) : The inertia weight.
        c1 (float) : The cognitive parameter.
        c2 (float) : The social parameter.
        losses (list) : A list of the best fitness values found during the optimization.
        """

        self.xwidth, self.ywidth, self.center, self.fitness = self.unpacker(citymap, fitness, stations=stations)
        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.losses = []

    def unpacker(self, citymap, fitness, stations=[]):
        """
        Formats the citymap and fitness function to be compatible with the PSO algorithm.

        Parameters
        ---
        citymap (list) : A list of coordinates (tuples). The first two should be the minimum and maximum corners of the search space.
                            The rest should be coordinates of the destination nodes.
        fitness (function) : The fitness function to be optimized. The function should take a dictionary of coordinates with the key being the type of node
                                and value being a list of the coordinates of the nodes, and return a float (time saved)
        stations (list) : A list of coordinates (tuples) of the stations

        Returns
        ---
        xwidth (float) : The width of the search space.
        ywidth (float) : The height of the search space.
        center (tuple) : The center of the search space.
        new_fitness (function) : The fitness function to be optimized. The function should take a list of station coordinates and return a float (time saved)
        """
        x1, y1 = citymap[0]
        x2, y2 = citymap[1]

        xwidth = np.abs(x2 - x1)
        ywidth = np.abs(y2 - y1)
        center = (x1 + x2) / 2, (y1 + y2) / 2

        coordinatelist = dict()
        coordinatelist['destination'] = citymap[2:]

        def new_fitness(swarm):
            coordinatelist['station'] = [(swarm[i], swarm[i+1]) for i in range(0, len(swarm), 2)]
            coordinatelist['station'] += stations
            return fitness(coordinatelist)
        return xwidth, ywidth, center, new_fitness
    
    def initswarm(self, num_particles, num_dimensions):
        """
        Initializes the swarm with random positions.

        Parameters
        ---
        num_particles (int) : The number of particles in the swarm.
        num_dimensions (int) : The number of dimensions of the search space.

        Returns
        ---
        swarm (numpy array) : A numpy array of shape (num_particles, num_dimensions) with random positions in the search space.
        """
        swarm = np.empty((num_particles, num_dimensions))
        for i in range(num_dimensions//2):
            swarm[:,i] = np.random.uniform(self.center[0] - self.xwidth/2, self.center[0] + self.xwidth/2, num_particles)
            swarm[:,i+1] = np.random.uniform(self.center[1] - self.ywidth/2, self.center[1] + self.ywidth/2, num_particles)
        
        return swarm
    
    def init_web_swarm(self, num_particles, num_dimensions, destinations):
        """
        Initializes the swarm such that every station is placed in between two random destinations

        Args
        ---
        num_particles (int) : The number of particles in the swarm.
        num_dimensions (int) : The number of dimensions of the search space.
        destinations (numpy array) : A numpy array of shape (num_destinations, 2) with the positions of the destinations.

        Returns
        ---
        swarm (numpy array) : A numpy array of shape (num_particles, num_dimensions) with random positions such that every station is placed in between two random destinations.
        """
        swarm = np.zeros((num_particles, num_dimensions))
        for i in range(num_particles):
            for j in range(0, num_dimensions, 2):
                np.random.shuffle(destinations)
                destination1 = destinations[0]
                destination2 = destinations[1]
                position_multiplier = np.random.uniform(0, 1)
                swarm[i,j] = (destination1 * position_multiplier + destination2 * (1 - position_multiplier))[0]
                swarm[i,j+1] = (destination1 * position_multiplier + destination2 * (1 - position_multiplier))[1]
        return swarm
        
    
    def optimize_PSO(self, num_particles, num_stations, num_iterations, progress = True):
        """
        Optimizes the fitness function using the PSO algorithm.

        Args
        ---
        num_particles (int) : The number of particles in the swarm.
        num_stations (int) : The number of new stations to optimize for in the search space.
        num_iterations (int) : The number of iterations the algorithm should run.

        Returns
        ---
        best_global_position (numpy array) : The best position found by the algorithm.
        best_global_fitness (float) : The fitness value of the best position found by the algorithm.
        """
        num_dimensions = num_stations*2
        swarm = self.initswarm(num_particles, num_dimensions)
        # swarm = self.init_web_swarm(num_particles, num_dimensions, stations)
        velocities = np.random.uniform(-self.xwidth*0.1, self.ywidth*0.1, (num_particles, num_dimensions))
        best_positions = swarm.copy()
        best_fitness = np.array([self.fitness(p) for p in swarm])
        best_global_position = best_positions[np.argmin(best_fitness)]
        best_global_fitness = np.min(best_fitness)
        
        for j in tqdm(range(num_iterations), disable = not(progress)):
            for i in range(num_particles):
                r1 = np.random.uniform(0, 1)
                r2 = np.random.uniform(0, 1)
                velocities[i] = self.w * velocities[i] + self.c1 * r1 * (best_positions[i] - swarm[i]) + self.c2 * r2 * (best_global_position - swarm[i])
                swarm[i] += velocities[i]
                fitness = self.fitness(swarm[i])
                if fitness < best_fitness[i]:
                    best_positions[i] = swarm[i]
                    best_fitness[i] = fitness
                    if fitness < best_global_fitness:
                        best_global_position = swarm[i]
                        best_global_fitness = fitness
            self.losses.append(best_global_fitness)
            if j % 10 == 0 and progress:
                print(f"Iteration {j}: Best fitness: {best_global_fitness}")

        return best_global_position, best_global_fitness
    
    def plot_losses(self):
        """
        Plots the losses of the optimization algorithm.

        Args
        ---
        None

        Returns
        ---
        None
        """
        plt.plot(self.losses)
        plt.xlabel("Iteration")
        plt.ylabel("Fitness")
        plt.title("Fitness over iterations")
        plt.show()
