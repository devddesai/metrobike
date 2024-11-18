# Metrobike project

## Introduction
In Austin, there are various metrobike stations placed throuhgout campus and wampus. The goal of this project is to find the most optimal placements of these stations and the number of bikes per station, while saving costs and maximizing the satisfaction of the users (see reward function to quantify satisfaction).

## Assumptions
- The population density of the area is known and can be used to determine the number of commuters at each location at any given time
- The commuting patterns of the population are independent of the availability of metrobikes
- Everyone is rational and will always choose the fastest mode of transportation


## Simulation setup
### Environment
The constants used in all environments are:
- `cost(n,b)`: the cost of building `n` stations with `b` bikes total
- `allowed_area`: the area where stations can be placed
- `bike_speed`: the speed of a bike
- `walking_speed`: the speed of a person walking
- `miles_per_charge`: the max mileage of a full charge
- `dt`: the time step of the simulation
- `new_commuter_prob`: the probability of a new commuter being added to the simulation at each time step
- `min_commuter_distance`: the minimum distance a commuter will travel

The following variables will be optimized:
- `n_stations`: the number of stations
- `total_bikes`: the total number of bikes in the system

### Required classes
The following classes are required for the simulation:
- `Station`: a class that represents a station
  - `location`: the location of the station
  - `n_bikes`: the max number of bikes at the station
  - `available_bikes`: a list of fully charged bikes at the station
  - `charging_bikes`: a list of bikes that are currently charging
  - `available_spots`: the number of spots available at the station
- `Bike`: a class that represents a bike
  - `Charge`: a float from 0 to 1 representing the charge of the bike
- `Commuter`: a class that represents a person travelling
  - `biking`: a boolean representing if the commuter is currently biking or walking
  - `position`: the current position of the commuter
  - `true_destination`: the true destination of the commuter
  - `station_destination`: the nearest availible station to the true destination
  - `bike`: the bike the commuter is currently using

### State space
The state space is defined by the following variables:
- `stations`: a list of stations
- `commuters`: a list of current commuters
- `population density`: a function that returns the population density at a given location. Can shift over time if needed.

### Observables
The observables are defined by the following variables:
- `total_cost`: the total cost of the stations
- `walked_distance`: the total distance walked by all commuters
- `biked_distance`: the total distance biked by all commuters

### Reward function
The reward function is defined as follows:
$$R = -\lambda_1 C + \lambda_2 \frac{T_b}{T}$$
where $C$ is the total cost of the stations, $T_w$ is the total distance walked by all commuters, and $T$ is the total distance travelled by all commuters (assuming that having access to a methro bike subscription will not change where you intend to travel). The $\lambda$ values are hyperparameters that can be tuned.

### Step function
The step function is defined as follows:
1. For each commuter use a pathfinding algorithm to determine shortest path to their true destination based on nearby, availible stations and bike/walk speed. Step the commuter along this path.
    - If the commuter is biking
      1. Update the charge of the bike 
      1. Update the `station_destination` of the commuter to the nearest available station to the true destination
      2. Invoke the `return_bike` function of the station
    - If the commuter is walking
      1. If the commuter has a non-null `station_destination` and is at the station, call the `rent_bike` function of the station
      2. If the commuter is at the true destination, remove them from the list of commuters
    - Update the `walked_distance` and `biked_distance` variables
2. Call the `charge_bikes` function of each station
3. Update the `population_density` function according to the time of day
4. With some probability `new_commuter_prob`, initialize a new commuter at a random location according to the `population_density` function at the current time and give them a random true destination according to the `population_density` function at a later time in the day (assume all commuters will travel some minimum distance `min_commuter_distance`)

### Functions to be implemented
The following functions need to be implemented:
- `return_bike`: a function that takes a commuter and a station, returns the commuter's bike to the station, and switches the commuter to walking mode
- `rent_bike`: a function that takes a commuter and a station and gives the commuter a bike from the station
- `charge_bikes`: a function that charges all bikes at the station, and updates the `available_bikes` and `charging_bikes` lists
- `pathfind`: a function that takes a commuter and a `true_destination` and returns a `station_destination` based on the availible stations and the `bike_speed` and `walking_speed` constants. If walking directly to the `true_destination` is the fastest option, the `station_destination` should be `None`.

### Optimization
For each environmental configuration, compute the reward at the end of the day. Then, implement some non-gradient based optimization algorithm to find the optimal configuration of
- `n_stations`
- `total_bikes`

## Considerations
- How the bikes should be placed initially is not clear. Maybe we can see how the distribution of bikes at some later time is influenced by the initial distribution of bikes. (if the effect is weak, we can simply randomly place the bikes and then run the simulation for one buffer day to get the optimal distribution)
- The population function needs to be periodic over a day
- The pathfinding algorithm should be as efficient as possible
- The above simulation is not optimized for speed at all, we should take care to save time/memory where possible

## Dev Updates
- Current functionality: System has a set # of agents, they move around to their destinations and instantly pick a new destination>
Next steps:
- Need to develop a good visualizer for the agents.
  - How to plot or show a graph, and then move agents along edges?
- Need to introduce stations
  - Putting stations at each node?
  - In each step, check if the station has enough space. If not, iterate through the model's pathfinder algorithm to find the closest station.