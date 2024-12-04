import numpy as np
from tqdm.notebook import tqdm

class PSO():
    """Particle Swarm Optimization
    
    
    Attributes:
        minval (float) : The minimum value of the search space.
        maxval (float) : The maximum value of the search space.
        fitness (function) : The fitness function to be optimized.
        w (float) : The inertia weight.
        c1 (float) : The cognitive parameter.
        c2 (float) : The social parameter.
    
    
    """

    
    
    def __init__(self, citymap, fitness, w, c1, c2):
        """Args:
            citymap (list) : A list of coordinates (tuples). The first two should be the minimum and maximum corners of the search space.
                             The rest should be coordinates of the destination nodes.
            fitness (function) : The fitness function to be optimized. The function should take a dictionary of coordinates with the key being the type of node
                                 and value being a list of the coordinates of the nodes, and return a float (time saved)
            w (float) : The inertia weight.
            c1 (float) : The cognitive parameter.
            c2 (float) : The social parameter.
        
        """

        self.minval, self.maxval, self.fitness = self.unpacker(citymap, fitness)
        self.w = w
        self.c1 = c1
        self.c2 = c2

    def unpacker(self, citymap, fitness):
        """
        Formats the citymap and fitness function to be compatible with the PSO algorithm.

        Args:
            citymap (list) : A list of coordinates (tuples). The first two should be the minimum and maximum corners of the search space.
                             The rest should be coordinates of the destination nodes.
            fitness (function) : The fitness function to be optimized. The function should take a dictionary of coordinates with the key being the type of node
                                 and value being a list of the coordinates of the nodes, and return a float (time saved)
        """
        x1, y1 = citymap[0]
        x2, y2 = citymap[1]
        minval = min(x1,y1)
        maxval = max(x2,y2)
        coordinatelist = dict()
        coordinatelist['destination'] = citymap[2:]
        def new_fitness(swarm):
            coordinatelist['station'] = [(swarm[i], swarm[i+1]) for i in range(0, len(swarm), 2)]
            return fitness(coordinatelist)
        return minval, maxval, new_fitness
    
    def initswarm(self, num_particles, num_dimensions):
        """
        Initializes the swarm with random positions.

        Args:
            num_particles (int) : The number of particles in the swarm.
            num_dimensions (int) : The number of dimensions of the search space.
        """
        return np.random.uniform(self.minval, self.maxval, (num_particles, num_dimensions))
    
    def optimize(self, num_particles, num_dimensions, num_iterations, progress = True):
        """
        Optimizes the fitness function using the PSO algorithm.

        Args:
            num_particles (int) : The number of particles in the swarm.
            num_dimensions (int) : The number of dimensions of the search space.
            num_iterations (int) : The number of iterations the algorithm should run.
        """
        num_dimensions*=2
        swarm = self.initswarm(num_particles, num_dimensions)
        velocities = np.random.uniform(-(self.maxval-self.minval)*0.1, (self.maxval-self.minval)*0.1, (num_particles, num_dimensions))
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
            if j % 10 == 0 and progress:
                print(f"Iteration {j}: Best fitness: {best_global_fitness}")

        return best_global_position, best_global_fitness
