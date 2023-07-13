import numpy as np
import networkx as nx
from matplotlib import pyplot as plt

# Converts networkx into dot file
def my_to_dot(nxgraph, out_fn, red_nodes=[]):
    with open(out_fn, 'w') as f:
        f.write("graph {\n")
        for i, j in nxgraph.edges:
            f.write("{0:4} -- {1:4}[label=\"{2:3.1f}\"]\n".format(i, j, real_graph[i][j]['weight']))
        for i in nxgraph.nodes:
            if i in red_nodes:
                f.write("{0:4}[color=\"red\", penwidth=5.0]".format(i))
        f.write("}\n")


# PARAMETERS
N_POINTS = 100   # Number of vertices in the real graph
N_MISSING = 10   # Number of vertices that will be taken out
DIMENSIONS = 2   # Dimension of the embedding
X_MAX = 100      # Range in each dimension (0 to X_MAX)
DISTANCE_THRESHOLD = 15   # Threshold for drawing an edge in the graph


# Alternative try starting from erdos graph, disregard
"""
real_graph = nx.fast_gnp_random_graph(N_POINTS, 0.05)
for i, j in real_graph.edges:
    real_graph[i][j]['weight'] = np.random.rand()*DISTANCE_THRESHOLD
my_to_dot(real_graph)
exit(1)
"""

# Generate points
coords = np.random.rand(N_POINTS, DIMENSIONS)*X_MAX  # random 3d coords in ([0,X_MAX], [0,X_MAX], [0,X_MAX])

# Compute real graph
real_graph = nx.Graph()
node_names = [str(i) for i in range(coords.shape[0])]
for i in node_names:
    real_graph.add_node(i)
for ii, i in enumerate(node_names):
    for jj, j in list(enumerate(node_names))[ii+1:]:
        d = np.linalg.norm(coords[ii] - coords[jj])
        if d < DISTANCE_THRESHOLD:
            real_graph.add_edge(i, j, weight=d)

# Choose vertices to hide
missing_vertices = np.random.choice(real_graph.nodes, size=N_MISSING, replace=False)
observed_vertices = sorted(list(real_graph.nodes - set(missing_vertices)))  # CAREFUL: elements are strings! To retrieve the corresponding index, use node_names.index(XXX) 


n_obs = len(observed_vertices)
observed_distances = np.zeros((n_obs, n_obs))

my_to_dot(real_graph, "real_graph.dot", red_nodes=missing_vertices)

# Distances defined along the paths: for Manpreet's algorithm
"""
for ii, i in enumerate(observed_vertices):
    for jj, j in list(enumerate(observed_vertices))[ii+1:]:
        p = nx.shortest_path(real_graph, i, j)
        p_length = 0
        for k in range(len(p)-1):
            p_length += float(real_graph[p[k]][p[k+1]]['weight'])
        print(i, j, p_length, nx.shortest_path(real_graph, i, j))
        observed_distances[ii, jj] = observed_distances[jj, ii] = p_length
"""

# Distances defined in the metric space: for Parth's algorithm
for ii, i in enumerate(observed_vertices):
    for jj, j in list(enumerate(observed_vertices))[ii+1:]:
        observed_distances[ii, jj] = observed_distances[jj, ii] = np.linalg.norm(coords[node_names.index(i)] - coords[node_names.index(j)])  


# Visualize on a 2d plane
x, y = list(zip(*[x for i, x in enumerate(coords) if node_names[i] in observed_vertices]))
x0, y0 = list(zip(*[x for i, x in enumerate(coords) if node_names[i] not in observed_vertices]))
plt.scatter(x, y)
plt.scatter(x0, y0, c='r')
plt.show()

# Distance matrix over knwon (blue) vertices
print("OBSERVED_DISTANCES")
print(observed_distances)