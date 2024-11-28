import networkx as nx
import numpy as np
import station as st

def square_vertices(s):
    """
    returns the vertices of a square centered at the origin. The square has dimensions (2s)x(2s)

    Parameters
    ---
    s: int
        scaling factor for the square

    Returns
    ---
    vertices: numpy array
        4x2 numpy array of vertices that make up a scaled 2x2 square. The vertices are ordered in a counter clockwise fashion starting from the top right vertex.
    """
    return np.array([[s, s], [-s, s], [-s, -s], [s, -s]])

def int_vertices(s):
    """ 
    returns the vertices of a rectangle centered at the origin. The rectangle has dimensions (8s)x(6s)
    
    Parameters
    ---
    s: int
        scaling factor for the rectangle

    Returns
    ---
    vertices: numpy array
        4x2 numpy array of vertices that make up a scaled 8x6 rectangle. The vertices are ordered in a counter clockwise fashion starting from the top right vertex.
    """
    return np.array([[3*s, 4*s], [-3*s, 4*s], [-3*s, -4*s], [3*s, -4*s]])

def basic_graph():
    """
    returns a basic graph with 4 stations and 4 destinations. Both stations and destinations are located at the vertices of a rectange centered at the origin. The station rectangle has dimensions 6x8 and the destination rectangle has dimensions 12x16. The first four nodes are the stations while the last four are destinations

    Parameters
    ---
    None

    Returns
    ---
    G: networkx graph
        graph with 8 nodes and 16 edges
    total_nodes: numpy array
        8x2 array of vertex locations. The first four are stations an`d the last four are destinations.
    """
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
        G.nodes[i]['data'] = st.Station(5, 1)
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
    """
    returns a basic weight vector for the basic graph. The weight vector is uniform

    Parameters:
    ---
    None

    Returns:
    ---
    weights: numpy array
        4x1 numpy array of weights to sample each destination with
    """
    return np.array([1, 1, 1, 1])/4
