import numpy as np

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
        self.minval, self.maxval, self.fitness = self.unpacker(citymap, fitness)
        self.w = w
        self.c1 = c1
        self.c2 = c2

    def unpacker(self, citymap, fitness):
        # NYI - Returns the range of coordinates available on the map and the fitness function
        minval = 0
        maxval = 0
        return minval, maxval, fitness
    
    def initswarm(self, num_particles, num_dimensions):
        return np.random.uniform(self.minval, self.maxval, (num_particles, num_dimensions))
    
    def optimize(self, num_particles, num_dimensions, num_iterations):
        swarm = self.initswarm(num_particles, num_dimensions)
        velocities = np.zeros((num_particles, num_dimensions))
        best_positions = swarm.copy()
        best_fitness = np.array([self.fitness(p) for p in swarm])
        best_global_position = best_positions[np.argmin(best_fitness)]
        best_global_fitness = np.min(best_fitness)
        
        for _ in range(num_iterations):
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
        return best_global_position, best_global_fitness
