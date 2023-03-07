import networkx as nx
import matplotlib.pyplot as plt

# Grafiğin oluşturulması
G = nx.Graph()

# Kenarların eklenmesi
G.add_edge('A', 'B', 4)
G.add_edge('B', 'C', 2)
G.add_edge('A', 'C', 1)

# Grafiğin çizdirilmesi
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos)
nx.draw_networkx_labels(G, pos)
nx.draw_networkx_edges(G, pos)
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, labels)

plt.show()
