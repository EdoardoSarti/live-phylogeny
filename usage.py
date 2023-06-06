import networkx as nx
import matplotlib.pyplot as plt
from smt import *
import numpy as np
from nj import *
from skbio import DistanceMatrix
from skbio.tree import nj



def SI(a,b):
    """returns SI value over non-gapped pairs"""
    matches = 0
    norm = 0
    for i in range(len(a)):
        if a[i] != '-' and b[i] != '-':
            norm += 1
            if a[i] == b[i]:
                matches+=1
    if norm == 0:
        return 0.
    return matches/norm

graph = nx.Graph()
in_f = open("data", "r")
leavesdict = {}
seqs = []
dates = []
line_count = 0
for line in in_f:
    seq, date_s = line.split()
    seqs.append(seq)
    dates.append(date_s.replace("_", "|"))
    leavesdict[date_s.replace("_","|")] = seq
    # graph.add_node(dates)
    line_count += 1
print(leavesdict)
print()
print()


dist_matrix = [[0] * line_count for _ in range(line_count)]

# print(dist_matrix)
for i in range(line_count):
    for j in range(i+1):
        dist_matrix[i][j] = 1-SI(seqs[i],seqs[j])
        dist_matrix[j][i] = 1-SI(seqs[i],seqs[j])

# Distance matrix made successfully at this point
print(dist_matrix)
dm = DistanceMatrix(dist_matrix, dates)
newick_str = nj(dm, result_constructor=str)
print(newick_str)
tree = nj(dm) # make tree using inbuild nj from skbio
print(tree.ascii_art()) # print tree

c_graph = nx.Graph()
for x in dates :
    c_graph.add_node(x)
for n1 in range (len(dates)):
    for n2 in range (len(dates)):
        c_graph.add_edge(dates[n1], dates[n2], distance = dm[n1][n2])


networkx_graph = skbio_tree_to_nx_graph(tree.root())        # tree to nx graph

# now to perform mst_steiner on this graph, choose the terminals
terminals = [node for node, degree in networkx_graph.degree() if degree == 1]         # set degree >= 1 if want to include all nodes, 
                                                                                      # else set to = 1 if want to include only the terminals
leaves = [node for node, degree in networkx_graph.degree() if degree == 1]
nodes = [node for node, degree in networkx_graph.degree() if degree >= 1]
for i in range (len(nodes)) :
    for j in range (i+1,len(nodes)) :
        d = nx.shortest_path_length(networkx_graph, nodes[i], nodes[j], weight='distance')
        networkx_graph.add_edge(nodes[i], nodes[j], distance=d)

        # if nodes[i] in leaves and nodes[j] in leaves :
        #     d = nx.shortest_path_length(networkx_graph, nodes[i], nodes[j], weight='distance')#1 - SI(leavesdict[nodes[i]], leavesdict[nodes[j]])
        #     if d < 1 :                                                                  # set to 1 if want to join all the leaves (clique)
        #         networkx_graph.add_edge(nodes[i], nodes[j], distance=d)
        # else :
        #     networkx_graph.add_edge(nodes[i], nodes[j], distance=nx.shortest_path_length(networkx_graph, nodes[i], nodes[j], weight='distance'))
print(terminals)
print(len(terminals)) # if this is correct, go ahead
print(networkx_graph)
print("Nodes:", networkx_graph.nodes)
print(len(networkx_graph.nodes))
print("Edges:", networkx_graph.edges)
# visualize_steiner_tree(networkx_graph,networkx_graph)

steiner_tree_nj = mst_steiner(networkx_graph, terminals)
# steiner_tree_normal = mst_steiner(c_graph, dates)


# def visualize_steiner_tree(steiner_tree, graph):
#     pos = nx.spring_layout(graph)  # Layout for node positioning
#     edge_labels = nx.get_edge_attributes(steiner_tree, 'distance')  # Get edge weights as labels
    
#     nx.draw_networkx(graph, pos, with_labels=True, node_color='lightblue', node_size=500, edge_color='gray')
#     nx.draw_networkx_edges(steiner_tree, pos, edgelist=steiner_tree.edges(), edge_color='red', width=2.0, alpha=0.5)
#     nx.draw_networkx_edge_labels(steiner_tree, pos, edge_labels=edge_labels)  # Display edge labels
#     plt.title("Steiner Tree")
#     plt.show()

print("NX GRAPH:", list(networkx_graph.edges(data=True)))
print("STEINER TREE:", list(steiner_tree_nj.edges(data=True)))


visualize_steiner_tree(steiner_tree_nj, steiner_tree_nj)
# visualize_steiner_tree(steiner_tree_normal, steiner_tree_normal)

# print("Nodes:", steiner_tree_nj.nodes)
# print(len(steiner_tree_nj.nodes))
# print("Edges:", steiner_tree_nj.edges)