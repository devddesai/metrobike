import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import station as st

#Sample stations (actual metrobike coordinates)
stations_coords = [
    (30.29068, -97.74292), #Nueces & 26th
    (30.283, -97.7375), # 21st & Speedway PCL
    (30.28395, -97.74198), # Guadalupe & 21st
    (30.28576, -97.74181), # UT West Mall @ Guad
    (30.28953, -97.73695), # Dean Keeton & Speedway
    (30.2874, -97.7478), # 23rd & San Gabriel

    (30.28354, -97.73953), # 21st & University
    (30.2862, -97.74516), # 22nd 1/2 Rio Grande
    (30.2853, -97.7467), # 22nd & Pearl
    (30.29333, -97.74412), # Rio Grande & 28th
    (30.2898, -97.74041), # Dean Keeton & Whitis
    (30.2856, -97.7335) # 23rd San Jac @ DKR Stadium
]

#destination points (picked out by me, subject to change)
destinations_coords = [
    (30.2910, -97.7430), #26 West
    (30.2843, -97.7372), #McCombs
    (30.2838, -97.7418), #Target
    (30.2865, -97.7410), #Union Building
    (30.2880, -97.7365), #PMA
    (30.2890, -97.7460), #Union on 24th

    (30.2885, -97.7375), #Welch
    (30.2895, -97.7425), #Rise
    (30.2895, -97.7470) #Axis West
    (30.2813, -97.7368), #Rec
]

def normalize_coords(station_coords, destination_coords):
    """
    finds the mean of the input station and destination coordinates and normalizes them

    Parameters:
    ---
    station coordinates and destination coordinates

    Returns:
    ---
    normalized_station_coords & normalized_destination_coordinates
        normalized the coordinates and added a scale of 10000/12
    """
    #find the mean of the coordinates
    sum_lat = 0
    sum_lon = 0
    for coord in station_coords:
        sum_lat += coord[0]
        sum_lon += coord[1]

    for coord in destination_coords:
        sum_lat += coord[0]
        sum_lon += coord[1]
    
    mean = (sum_lat/(len(station_coords) + len(destination_coords)), sum_lon/len(station_coords) + len(destination_coords))


    #normalize the coordinates
    normalized_station_coords = []
    normalized_destination_coords = []

    for coord in station_coords:
        normalized_station_coords.append(10*(coord[0] - mean[0], coord[1] - mean[1]))
    
    for coord in destination_coords:
        normalized_destination_coords.append(10*(coord[0] - mean[0], coord[1] - mean[1]))
    return normalized_station_coords, normalized_destination_coords

def weights():
    """
    returns a weight vector for the graph based on probabilities at end destination.

    these probabilities are based on count of visits at return metrobike stations, pulled from the metrobike api. 

    Parameters:
    ---
    None

    Returns:
    ---
    weights: numpy array
        10x1 numpy array of weights to give probability of agent heading to that destination
    """
    end_station_visits = {"Nueces & 26th":56842, "Speedway @PCL":183345,"Guad & 21st":63373, "UT West Mall @ Guad": 63044,  "Dean Keeton & Speedway":100716, "23rd & San Gabriel": 52221, "Dean Keeton & Whitis": 16679,  "21st University":183345,"22nd 1/2 Rio Grande": 15691, "23rd & San Jac @ DKR": 40974, "22nd & Pearl":50072, "28th rio grande":52104 }

    total_visits = sum(end_station_visits.values())

    end_dest_probabilities = {"26th West": 56842/total_visits,
                          "McCombs": 183345/total_visits,
                          "Target":63373/total_visits,
                          "Union Building":63044/total_visits,
                          "PMA":100716/total_visits,
                          "Union on 24th":52221/total_visits,

                          "Welch":100716/total_visits,
                          "Rise":15691/total_visits,
                          "Axis West":56482/total_visits,
                          "Rec":40974/total_visits}
    

    
    return np.array(list(end_dest_probabilities.values()))

#FUNC 1

#station_coords and destination_coords are both a list of tuples
def create_graph_from_coordinates(stations_coords, destinations_coords):
    """
    creates a networkx graph with edges in between the station and destination nodes

    Parameters:
    ---
    station coordinates and destination coordinates

    Returns:
    ---
    G
        the networkx graph object
    station_nodes
        a dictionary of station nodes with their positions, types (station), and datas (station class attributes)
    destination_nodes
        a dictionary of destination nodes with their positions, types (destinations), and datas (None) 
    """
    total_nodes = np.array(stations_coords + destinations_coords)

    #distance calculation from hasith
    distances = np.zeros((total_nodes.shape[0], total_nodes.shape[0]))
    for i in range(total_nodes.shape[0]):
        for j in range(i + 1, total_nodes.shape[0]):
            distances[i, j] = np.linalg.norm(total_nodes[i] - total_nodes[j])
            distances[j, i] = distances[i, j]

    G = nx.Graph()

    #add stations
    for i, coord in enumerate(stations_coords):
        G.add_node(f"Station {i+1}", pos=(coord[1], coord[0]), type='station', data=st.Station(5, 3))

    #add destination nodes
    for i, coord in enumerate(destinations_coords):
        G.add_node(f"Destination {i+1}", pos=(coord[1], coord[0]), type='destination', data=None)

    #add edges
    all_nodes = list(G.nodes)
    for i in range(len(all_nodes)):
        for j in range(i + 1, len(all_nodes)):
            G.add_edge(all_nodes[i], all_nodes[j], weight=distances[i, j])

    #positions of nodes
    pos = nx.get_node_attributes(G, 'pos')

    node_colors = ['lightblue' if G.nodes[node]['type'] == 'station' else 'red' for node in G.nodes]
    plt.figure(figsize=(10, 8))
    nx.draw(G, pos, with_labels=True, node_size=500, node_color=node_colors)
    plt.title("NetworkX Graph of Stations and End Destinations")
    plt.show()

    #create dicts for station+nodes and destination_nodes
    station_nodes = {node: data for node, data in G.nodes(data=True) if data['type'] == 'station'}
    destination_nodes = {node: data for node, data in G.nodes(data=True) if data['type'] == 'destination'}

    return G, station_nodes, destination_nodes