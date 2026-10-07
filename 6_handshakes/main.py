import matplotlib
import scipy.stats as ss

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

G = nx.read_edgelist("facebook/0.edges", nodetype=int, create_using=nx.Graph())

nodes = list(G.nodes())
shortest_paths = dict(
    nx.all_pairs_all_shortest_paths(G, weight=None, method="unweighted")
)
distribution = []
for node in nodes:
    node_paths = shortest_paths[node]
    for destination in node_paths.keys():
        for path in node_paths[destination]:
            distribution.append(len(path) - 1)
distribution = np.array(distribution)
mode = ss.mode(distribution)
median = np.median(distribution)
print(f"Мода: {mode.mode}. Встречается {mode.count} раз\n")
print(f"Медиана: {median}\n")
plt.figure(figsize=(8, 6))
plt.title("Распределение длин кратчайших путей между двумя вершинами")
plt.xlabel("Длина пути")
plt.ylabel("Количество путей")
plt.hist(distribution)
plt.show()
