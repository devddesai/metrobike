import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


def create_random_graph(nodes, max_length, prob=0.5):
    g = nx.gnp_random_graph(nodes, prob)
    for (u,v) in g.edges():
        g.edges[u,v]['weight'] = np.random.randint(1, max_length)
    return g


# g=create_random_graph()
# nx.draw(g, with_labels=True, node_color='skyblue', node_size=500, font_size=10)
# plt.show()