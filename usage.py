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
    line_count += 1
# print(leavesdict)

dist_matrix = [[0] * line_count for _ in range(line_count)]

for i in range(line_count):
    for j in range(i+1):
        dist_matrix[i][j] = 1-SI(seqs[i],seqs[j])
        dist_matrix[j][i] = 1-SI(seqs[i],seqs[j])

# Distance matrix made successfully at this point
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

steiner_tree_nj = mst_steiner(networkx_graph, terminals)
visualize_steiner_tree(steiner_tree_nj, steiner_tree_nj)
