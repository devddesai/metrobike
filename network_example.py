import networkx as nx
import numpy as np
import station as st

def square_vertices(s):
    return np.array([[s, s], [-s, s], [-s, -s], [s, -s]])

def int_vertices(s):
    return np.array([[3*s, 4*s], [-3*s, 4*s], [-3*s, -4*s], [3*s, -4*s]])

def basic_graph():
    stations = int_vertices(1)
    destinations = int_vertices(2)

    n_stations = stations.shape[0]
    n_destinations = destinations.shape[0] 

    total_nodes = np.concatenate((stations, destinations), axis=0)
    distances = np.zeros((total_nodes.shape[0], total_nodes.shape[0]))
    for i in range(total_nodes.shape[0]):
        for j in range(i+1, total_nodes.shape[0]):
            distances[i,j] = np.linalg.norm(total_nodes[i] - total_nodes[j])
            distances[j,i] = distances[i,j]

    # make graph from distances as adjacency matrix
    G = nx.Graph()
    for i in range(n_stations):
        G.add_node(i)
        G.nodes[i]['type'] = 'station'
        G.nodes[i]['data'] = st.Station(5, np.random.randint(0,6))
    for i in range(n_stations, n_stations+n_destinations):
        G.add_node(i)
        G.nodes[i]['type'] = 'destination'
        G.nodes[i]['data'] = None # TODO: edit this later

    for i in range(total_nodes.shape[0]):
        for j in range(i+1, total_nodes.shape[0]):
            G.add_edge(i, j, weight=distances[i,j])
            # For asymmetric distances
            # G.add_edge(j, i, weight=distances[j,i])

    return G, total_nodes

def basic_weights():
    return np.array([1, 1, 1, 1])/4
