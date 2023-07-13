import networkx as nx
import matplotlib.pyplot as plt
from smt import *
import numpy as np
from nj import *
from skbio import DistanceMatrix
from skbio.tree import nj
from networkx.drawing.nx_agraph import write_dot
import skbio

# RUN this Usage file with data in the 'data' file in same directory

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
print(tree.ascii_art(show_internal = True)) # print tree
# print(tree.find("ancestor").parent)
tree2 = tree.root_at(tree.find("ancestor").parent)
print(tree2.ascii_art()) # print tree






networkx_graph = skbio_tree_to_nx_graph(tree.root())        # tree to nx graph
terminals = [node for node, degree in networkx_graph.degree() if degree == 1]         # set degree >= 1 if want to include all nodes, 
# visualize_steiner_tree(networkx_graph,networkx_graph)


nodes = [node for node, degree in networkx_graph.degree() if degree >= 1]
names = []
dist_mat = np.zeros((len(nodes), len(nodes)))
n,m = 0,0
L =[]
for i in range (len(nodes)) :
    names.append(nodes[i])
    for j in range (i+1,len(nodes)) :
        if (nodes[i] in dates and nodes[j] in dates) : 
            n += 1
            # d = max((1-SI(leavesdict[nodes[i]],leavesdict[nodes[j]])), nx.shortest_path_length(networkx_graph, nodes[i], nodes[j], weight='distance'))
            # d = nx.shortest_path_length(networkx_graph, nodes[i], nodes[j], weight='distance')
            d = 1-SI(leavesdict[nodes[i]],leavesdict[nodes[j]])
            # if ((1-SI(leavesdict[nodes[i]],leavesdict[nodes[j]]))> nx.shortest_path_length(networkx_graph, nodes[i], nodes[j], weight='distance')) : m += 1
            # L.append((1-SI(leavesdict[nodes[i]],leavesdict[nodes[j]]))/nx.shortest_path_length(networkx_graph, nodes[i], nodes[j], weight='distance'))
            dist_mat[i][j] = dist_mat[j][i] = d
            networkx_graph.add_edge(nodes[i], nodes[j], weight = d)
        else :
            d = nx.shortest_path_length(networkx_graph, nodes[i], nodes[j], weight='weight')
            dist_mat[i][j] = dist_mat[j][i] = d
            networkx_graph.add_edge(nodes[i], nodes[j], weight = d)
    # visualize_steiner_tree(networkx_graph,networkx_graph)

datanodes = []
for ii in range (len(nodes)) : 
    if nodes[ii] in dates : 
        datanodes.append(ii)
print(datanodes)
print(dist_mat)

print(m/n)
print(L)
results = np.array(L)

print("Var", np.var(results))
print("Mean", np.mean(results))
print("Median", np.median(results))




# now to perform mst_steiner on this graph, choose the terminals
# terminals = [node for node, degree in networkx_graph.degree() if degree == 1]         # set degree >= 1 if want to include all nodes, 
                                                                                      # else set to = 1 if want to include only the terminals
# terminals = set(terminals1) - 
leaves = [node for node, degree in networkx_graph.degree() if degree == 1]
nodes = [node for node, degree in networkx_graph.degree() if degree >= 1]
# for i in range (len(nodes)) :
#     for j in range (i+1,len(nodes)) :
#         # d = nx.shortest_path_length(networkx_graph, nodes[i], nodes[j], weight='distance')
#         d = dist_mat[i][j]
#         networkx_graph.add_edge(nodes[i], nodes[j], distance=d)
print("Leavesdict and terminals", leavesdict, terminals)
print("Input graph is", networkx_graph)
steiner_tree_nj = mst_steiner(networkx_graph, terminals, leavesdict)
write_dot(steiner_tree_nj,'./out')
# steiner_tree_normal = mst_steiner(c_graph, terminals)
# visualize_steiner_tree(steiner_tree_normal, steiner_tree_normal)
visualize_steiner_tree(steiner_tree_nj, steiner_tree_nj)
