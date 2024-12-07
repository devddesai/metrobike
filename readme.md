### 4 stations

![Alt text](/devimages/4_2__0.7_0.1_.png "4 station configuration")
- this is the 4 station configuration

# genetic
![Alt text](/devimages/genetic_algorithm_4_2_1weight.png "G4 destinations, 2 stations, Station 1 favored")

- this is for 4 stations, 2 destinations. weights= (0.7,0.1,0.1,0.1). station favored the higher probability station 1, and also the station opposite?

![Alt text](/devimages/genetic_algorithm_4_2_2weight.png "G4 destinations, 2 stations, Station 2 favored")
- weights = (0.1,0.7,0.1,0.1)
- favored 2, but idk why it specifically favored 3, maybe its random, i expected it to be the opposite one.
- i ran it again in the bottom pic, and it favored 2 and 1 which points to randomness

![Alt text](/devimages/genetic_algorithm_4_2_2weightp2.png "G4 destinations, 2 stations")
- weights = (0.1,0.7,0.1,0.1)
- ran 2 favored again, and the other station was 1, unlike 3 above, shows that ones station is placed to the favored station, and if all others are equal weights, the other station will be placed close randomly to another destination

# PSO
![Alt text](/devimages/PSO_4_2_2weight.png "PSO 4 destinations, 2 stations")
- weight [0.1, 0.7, 0.1, 0.1]
- looks good, again station 2 is on the top which makes sense, station favored destination 2

![Alt text](/devimages/PSO_4_4_2weight.png "PSO 4 destinations, 4 stations")
- shows the failure of 4x4 PSO 


### 2 stations
# genetic
![Alt text](/devimages/genetic_alg_2_2.png "G2 destinations, 2 stations")
- expected

![Alt text](/devimages/PSO_2_2_2weight.png "PSO 2 destinations, 2 stations")
- expected


### Invariance to initial bike distribution: histograms
- heres the station/destination configuration for this analysis
![Alt text](/devimages/networkexample.png)

- started with all 10 bikes at station 1, but distribution of 10,000 steps is equal; shows convergence
- equal probability distribution
![Alt text](/devimages/hst0.png)
![Alt text](/devimages/hst1.png)
![Alt text](/devimages/hst2.png)
![Alt text](/devimages/hst3.png)

- here's the animation showing the convergence, very quickly the bikes leave the initial distribution, within a couple 10's of steps
![Alt text](/devimages/bike_distribution.gif)


- Here's the same analysis, with bike distribution: (10, 0, 0, 0), but instead of equal weights, w = (0.7, 0.1, 0.1, 0.1)
- Animation: 
![Alt text](/devimages/skewbike.gif)
- Distributions: note how, as expected due to the skewed PDF, station 0 has high traffic
![Alt text](/devimages/skewst0.png)
![Alt text](/devimages/skewst1.png)
![Alt text](/devimages/skewst2.png)
![Alt text](/devimages/skewst3.png)