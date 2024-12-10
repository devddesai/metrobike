# Instructions
To run the code, first install the required packages using the following command:
```bash
pip install -r requirements.txt
```
Then, you can take a look at the notebook `metrobike.ipynb` to see the code in action. The notebook will guide you through the process of running the simulations and visualizing the results.

# Quick Start
To test the optimizer, you can copy the following code into a python file or jupyter notebook. This code will run fine on its own, but if you would like to add your own destinations, modify the `citymap ` and `weights` accordingly. Keep in mind that the first two coordinates of `citymap` are the bottom left and top right corners of a rectangle containing the region you want to allow stations to be placed, in any order.
```bash
import networkx as nx
import pandas as pd

import network_example as ne
import graph_utils as gu
import matplotlib.pyplot as plt
import optimize as ogf
import model as m

# Define citymap
citymap = [(-6, -6), (6, 6), (0, -4.5), (0, 4.5)]

# Define weights - should be same length as number of destinations, weights should add up to 1
w = [0.5, 0.5]

# Define fitness
def fitness_from_coords(coordinate_list, agents, weights, seed=1, n_steps=1000):
    """
    Fitness function for the optimization problem, returns the negative of the average number of trips per agent

    Parameters:
    ---
    coordinate_list: dict
        Dictionary containing the coordinates of the stations and destinations
    agents: int
        Number of agents in the model
    weights: list
        List of weights for the destinations
    seed: int
        Random seed for the model
    n_steps: int
        Number of steps to run the model for

    Returns:
    ---
    float
        Negative of the average number of trips per agent
    """
    destinations = coordinate_list["destination"]
    stations = coordinate_list["station"]
    G, s, d = gu.create_graph_from_coordinates(stations, destinations)
    model = m.MyModel(agents, seed=seed, G=G, weights=weights)
    for i in range(n_steps):
        model.step()
    return -1*model.trips_average()

def fitness(agents, weights, seed=1, n_steps=1000):
    """
    Returns a lambda function that takes a list of coordinates and returns the fitness value. 
    Used as the fitness function for the optimizer class since it only accepts functions with 
    one parameter of destination coordinates

    Parameters:
    ---
    agents: int
        Number of agents in the model
    weights: list
        List of weights for the destinations
    seed: int
        Random seed for the model
    n_steps: int
        Number of steps to run the model for

    Returns:
    ---
    lambda
        Lambda function that takes a list of coordinates and returns the fitness value
    """
    return lambda x: fitness_from_coords(x, agents, weights, seed, n_steps)

# Create graph for visualization
G,s,d = gu.create_graph_from_coordinates([], citymap[2:])

pos = {i: d["Destination " + str(i+1)] for i in range(len(d))}
print(pos)
colors = ['r' if G.nodes[i]['type'] == 'destination' else 'b' for i in G.nodes]
nx.draw_networkx(G, {"Destination 1": [0, -4.5], "Destination 2": [0, 4.5]}, node_color = colors, with_labels=True)
plt.show()

# Run optimizer
optimizer = ogf.Optimize(citymap, fitness(agents=20, weights=w, seed=1, n_steps=100), w=0.7, c1=1.4, c2=1.4, mutation_rate=0.7, alpha=0.3)
bestpos, bestfit = optimizer.optimize_PSO(20, 2, 50)

## uncomment for genetic algorithm
# bestpos, bestfit = optimizer.optimize_genetic(num_particles=20, num_dimensions=2, num_iterations=50)

# Plot loss curve
optimizer.plot_losses()

print("Best solution found:", bestfit)
stations = [(bestpos[i], bestpos[i+1]) for i in range(0, len(bestpos), 2)]
# print(stations)
G, s, d, = gu.create_graph_from_coordinates(stations, citymap[2:])

# Plot final result
plt.scatter([station[0] for station in stations], [station[1] for station in stations], c='red', label='Stations')
plt.scatter([destination[0] for destination in citymap[2:]], [destination[1] for destination in citymap[2:]], c='blue', label='Destinations')
plt.xlabel('X-Coordinate')
plt.ylabel('Y-Coordinate')
plt.xlim(-6, 6)

plt.title('PSO: 2 stations, 2 destinations')
plt.legend()
# plt.savefig('PSO_2_2_2weight.png')
plt.show()
```

## Project Structure
The project is structured as follows:
- `bike_visualizations.py`: Containins the functions used to visualize the bike distributions.
- `commuter.py`: Containins the Commuter class used as each agent in the simulation.
- `graph_utils.py`: Contains the functions used in the project.
- `metrobike.ipynb`: Jupyter notebook containing the code for running the simulations and visualizing the results.
- `model.py`: Contains the MyModel class used as the main class for the ABM simulation with the Mesa library.
- `network_example.py`: Contains code to quickly generate and probe a toy network of destinations and stations.
- `optimize.py`: Contains the the class used to run the optimization algorithms of the particle swarm optimization and the genetic algorithm.
- `pathfinding.py`: Contains the functions used to find the shortest path (in terms of time needed) between two nodes in the network.
- `station.py`: Contains the Station class used to represent each station in the simulation.

# Introduction
The goal of this project is to simulate the behavior of a bike-sharing system in a network of stations and destinations, and then optimize the positions of the stations. 

## The Model
The model consists of a number of stations where bikes can be picked up and dropped off, and a number of destinations that agents (commuters) want to visit. This is reprsented by a graph that agents can traverse.

For example, consider the following graph:

![Alt text](/images/networkexample.png)

In this graph, the blue nodes represent destinations and the red nodes represent stations. Every node is connected to every other node by an edge, whose weight represents the time it takes to travel between them on a bike (to get the time between two nodes by walking, multiply the edge weight by 3 since walking is about 3 times slower than biking). The fact that the graph is fully connected means that, in principle, an agent can travel between any two nodes by walking.

If an agent wants to bike, however, they must find a station with an available bike and another station where they can return the bike (ideally, the agent would want to find a station close to their destination to drop off the bike). Based on the fact that stations can be full or empty, the agent must decide whether to walk or bike to their destination. The full logic of the agent's pathfinding can be found in the `pathfinding.py` file and the `step` method in the `Commuter` class in `commuter.py`. 

At each timestep, the agents move towards their destination, and the stations update their bike counts based on the agents' decisions. The way agents choose a particular destination is based on a probability distribution that we can set. Using the previous graph as an example, we can set the probability distribution to be uniform for every destination, or we can set it so that agents favor certain destinations over others. This is done with the `weights` attribute in the `MyModel` class in `model.py`.

## Optimization
The goal of the optimization is to find the best positions for the stations in the network. We can use two algorithms to do this: particle swarm optimization (PSO) and a genetic algorithm (GA). The optimization algorithms are implemented in the `optimize.py` file.

Essentially, we treat the position of all $n$ stations we want to optimize as a single vector $x \in \mathbb{R}^{2n}$, where each station has an $(x, y)$ coordinate. So, the optimization problem is to find the best $x$ that minimizes a fitness function. The fitness function we use is the negative of the average trips completed per agent, which we denote as $L$:
$$L = -\frac{T}{N}$$
where $T$ is the total number of trips completed by all agents and $N$ is the number of agents in the model. The reason we use the negative of the average trips completed is because the optimization algorithms are designed to minimize the fitness function, and we want to maximize the number of trips completed.

### PSO
Our implementation of PSO has the following hyperparameters:
- `n_particles`: The number of particles in the swarm.
- `n_iterations`: The number of iterations the algorithm will run for.
- `c1`: The cognitive parameter.
- `c2`: The social parameter.
- `w`: The inertia parameter.

The PSO algorithm works by initializing a swarm of particles with random positions and velocities. At each iteration, the particles update their positions and velocities based on their best position so far and the best position of the swarm. The best position of the swarm is the position that minimizes the fitness function. The particles then update their positions based on the following formula:
$$v_{i+1} = wv_i + c_1r_1(p_{\text{best}, i} - x_i) + c_2r_2(g_\text{best} - x_i)$$
$$x_{i+1} = x_i + v_{i+1}$$
where $v_i$ is the velocity of particle $i$, $x_i$ is the position of particle $i$, $p_{\text{best}, i}$ is the best position of particle $i$ so far, $gbest$ is the best position of the swarm, $r_1$ and $r_2$ are random numbers between 0 and 1, and $w$, $c_1$, and $c_2$ are the inertia, cognitive, and social parameters, respectively.

The PSO algorithm will do this for `n_iterations` iterations, and at the end, it will return the best position of the swarm found so far.

### Genetic Algorithm
Our implementation of the genetic algorithm has the following hyperparameters:
- `population_size`: The number of individuals in the population.
- `n_generations`: The number of generations the algorithm will run for.
- `mutation_rate`, $p$: The probability that a gene will mutate.
- `alpha`: The strength of the mutation.

Genetic algorithms works by initializing a population of individuals with random genes. At each generation, the individuals are evaluated based on their fitness, and the best individuals are selected to reproduce. The reproduction process involves selecting two parents and creating a child by combining their genes. The child's genes are then mutated with a certain probability. The best individuals from the previous generation are carried over to the next generation. The genetic algorithm will do this for `n_generations` generations, and at the end, it will return the best individual found so far.

In our case, the genes of an individual is a vector of $2n$ elements, where each pair of elements represents the $(x, y)$ coordinate of a station out of $n$ total stations. The fitness of an individual is the negative of the average trips completed per agent, as defined above. Given the two fittest individuals, $a$ and $b$, the child's genes are given by:
$$c_i = \left[\begin{cases}
    a_i  & \text{with probability } 0.5 \\
    b_i & \text{with probability } 0.5
\end{cases}\right] + 
\begin{cases}
    \alpha B & \text{with probability } p \\
    0 & \text{with probability } 1 - p
\end{cases}
$$
where $B$ is the length of the maxiumum dimension of the search space, $p$ is the mutation rate, and $\alpha$ is the strength of the mutation.

# Results
Everything needed to reproduce the results can be found in the `metrobike.ipynb` notebook. The notebook will guide you through the process of running the simulations and visualizing the results.

## Simple 2 station, 2 destination case
This is the simplest case we can consider. Here, the analytical solution is quite simple to find if we assume uniform weights for the destinations. The optimal positions for the station are to place them directly on top of the destinations, and both PSO and GA are able to find this solution quite easily:

![Alt text](/images/pso_2_2.png "PSO 2 destinations, 2 stations")
![Alt text](/images/ga_2_2.png "G2 destinations, 2 stations")

## 4 station, 2 destination case
For this case, we placed four destinations in a diamond shape. And destinations 2 and 1 are about twice as far away from each other than destination 3 and destination 4.

![Alt text](/images/diamond.png "4 station configuration")

Thus, with only two stations to place, the optimal solution is to place one station near destination 2 and the other near destination 1. Both the PSO and the genetic algorithm are quite sensitive to this problem, it seems as if they only converge to the optimal solution about half the time. For the PSO, we show a failed case, and for the GA we show a successful case where the optimal solution was found:

![Alt text](/images/pso_4_2_uniform.png "PSO 4 destinations, 2 stations")
![Alt text](/images/ga_4_2_uniform.png "GA 4 destinations, 2 stations")

Additionally, we can also consider the case where the weights are not uniform. For example, we can set the weights to be $(0.7, 0.1, 0.1, 0.1)$. In this case, the optimal solution is to place one station near destination 2 and the other near destination 1, since destination 1 will be the most popular. In this case, both PSO and GA are able to find the optimal solution:

![Alt text](/images/pso_4_2_1weight.png "PSO 4 destinations, 2 stations")
![Alt text](/images/ga_4_2_1weight.png "GA 4 destinations, 2 stations")

## 4 station, 4 destination case
For this case, we placed four destinations in a square shape. The optimal solution is to place one station near each destination. However, both algorithms fail to find the optimal solution nearly every time and give us something like the following result:

![Alt text](/images/pso_4_4.png "PSO 4 destinations, 4 stations")

This is likely due to the fact that for this case, the optimal solution is hidden behind many local minima, and the algorithms are not able to escape them. It could be possible that more aggresive methods to jump out of local minima could help for this particular case of destinations=stations.

## Invariance to initial bike distribution
As one would expect, the initial distribution of bikes at the stations does not affect the final distribution of bikes at the stations. This is shown in the following histograms, where we start with all 10 bikes at station 1, but the distribution of bikes at the stations after 10,000 steps is equal (distribution collected for a model with 4 stations and 4 destinations, each with uniform weights):

![Alt text](/images/uniformhist.PNG)

We can also alter the weights of the destinations to be $(0.7, 0.1, 0.1, 0.1)$ and observe how the invariant distribution is altered:

![Alt text](/images/skewhist.PNG)

Even without seeing the actual map we used (we used the basic example graph shown in the very beginning), one can already guess that station 0 was placed closes to the most popular destination since it has the heaviest tail towards the right. From there, the agents seemed to prefer to bike to station 2 more often than station 3, and hardly any bikes ever reached station 1. So, despite station 1, 2, and 3 being just as popular of a destination, station 1 could had much less bikes than stations 2 or 3. 

Thus, we can see that the popularity of a destination is not the only factor that determines the distribution of bikes at nearby stations--we also need to consider the practicality riding a bike towards that destination from other nearby, popular destinations.

# Application to Real-World Data
Using metrobike data, we were able to estimate how popular certain areas in Austin were, and using GIS data of the distances between select locations of around campus and west campus, we were able to create a graph to represent UT Austin. 

![Alt text](/images/destination_configuration.png "10 destination configuration")

The select locations and their respective weights we used were (the list number corresponds to the destination number of the graph):
1. 26th West - 0.078
2. McCombs - 0.25
3. Target - 0.086
4. Union Building - 0.086
5. PMA - 0.14
6. Union on 24th - 0.071
7. Welch - 0.14
8. Rise - 0.021
9. Axis West - 0.077
10. Rec - 0.056

Then, we were able to use our optimization algorithms to find the optimal positions of the stations. We optimized for 6 stations around campus and west campus, and the results can be seen in the following images:

![Alt text](/images/genetic10x6.png)
![Alt text](/images/pso10x6.png)

We can see that the PSO algorithm was able to place all 6 stations within the boundaries we set, while the genetic algorithm placed 2 stations outside of the boundaries. In fact, the PSO solution seems very reasonable, with stations placed near the most popular destinations!

# Conclusion
For small systems, the optimization algorithms are able to find the optimal solution quite easily and quickly. For larger systems, however, we begin to see convergence issues. Nevertheless, given enough different initial conditions, the algorithms are able to find the optimal solution eventually--still faster than trying to brute force the solution as we allowed for a continious search of a $2n$ dimensional space, where $n$ is the number of stations whose locations we want to optimize.

We were able to find some interesting relationships between the popularity of a destination and the distribution of bikes at nearby stations. We also found that the initial distribution of bikes at the stations does not affect the final distribution of bikes at the stations, so the model has an invariant distribution of bikes that is reached rather quickly.

Finally, we were able to apply our model to real-world data and find the optimal positions of stations around campus and west campus. The results were quite reasonable, with stations placed near the most popular destinations.

# Future Work
Some directions we would really like to explore are
- Implementing a diurnal function to change the weights of destinations over time
- Implement a more agressive method to escape local minimas, which could help us find more optimal solutions for larger systems
- Visualizing the paths agents take to reach their destinations
- Do a grid search to find the best hyperparameters for the optimization algorithms, maybe this could also help stabilize convergence for larger systems
