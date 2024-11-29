import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import station as st

#Sample stations (actual metrobike coordinates)
stations_coords = [
    (30.29068, -97.74292),
    (30.2862, -97.74516),
    (30.2874, -97.7478),
    (30.28395, -97.74198),
    (30.28576, -97.74181),
    (30.2853, -97.7467),
    (30.29333, -97.74412),
    (30.28953, -97.73695),
    (30.2898, -97.74041),
    (30.28354, -97.73953),
    (30.283, -97.7375),
    (30.2856, -97.7335)
]

#destination points (picked out by me, subject to change)
destinations_coords = [
    (30.2843, -97.7372), #McCombs
    (30.2813, -97.7368), #Rec
    (30.2838, -97.7418), #Target
    (30.2895, -97.7425), #Rise
    (30.2910, -97.7430), #26 West
    (30.2890, -97.7460), #Union on 24th
    (30.2880, -97.7365), #PMA
    (30.2865, -97.7410), #Union Building
    (30.2885, -97.7375), #Welch
    (30.2830, -97.7360) #Greg
]

#FUNC 1

#station_coords and destination_coords are both a list of tuples
def create_graph_from_coordinates(stations_coords, destinations_coords):

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
        G.add_node(f"Destination {i+1}", pos=(coord[1], coord[0]), type='end_destination', data=None)

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

    #create dicts for station+nodes and end_destination_nodes
    station_nodes = {node: data for node, data in G.nodes(data=True) if data['type'] == 'station'}
    end_destination_nodes = {node: data for node, data in G.nodes(data=True) if data['type'] == 'end_destination'}

    return G, station_nodes, end_destination_nodes

#FUNC 2

#station_coords and destination_coords are both a list of tuples
def create_graph_from_stations(stations_coords):

    destinations_coords = [
    (30.2843, -97.7372), #McCombs
    (30.2813, -97.7368), #Rec
    (30.2838, -97.7418), #Target
    (30.2895, -97.7425), #Rise
    (30.2910, -97.7430), #26 West
    (30.2890, -97.7460), #Union on 24th
    (30.2880, -97.7365), #PMA
    (30.2865, -97.7410), #Union Building
    (30.2885, -97.7375), #Welch
    (30.2830, -97.7360) #Greg
    ]

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
        G.add_node(f"Destination {i+1}", pos=(coord[1], coord[0]), type='end_destination', data=None)

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

    #create dicts for station+nodes and end_destination_nodes
    station_nodes = {node: data for node, data in G.nodes(data=True) if data['type'] == 'station'}
    end_destination_nodes = {node: data for node, data in G.nodes(data=True) if data['type'] == 'end_destination'}

    return G, station_nodes, end_destination_nodes
