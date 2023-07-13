# TESTS FOR TOY MODEL (MADE BY HAND/ON-PAPER)

from treeGen import *
import networkx as nx
from smt import *
import matplotlib.pyplot as plt
from skbio import DistanceMatrix
from skbio.tree import nj
from nj import *
from networkx.drawing.nx_pydot import write_dot
import numpy as np

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


dm4 = [[0,3,1,4.5,5.5], [3,0,2,5.5,6.5], [1,2,0,3.5,4.5], [4.5,5.5,3.5,0,2], [5.5,6.5,4.5,2,0]]
# dm3 = [[0,3,1,4.5,5.5], [3,0,2,5.5,6.5], [1,2,0,3,4.5], [4.5,5.5,3,0,2], [5.5,6.5,4.5,2,0]]



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
print(leavesdict)

dist_matrix = [[0] * line_count for _ in range(line_count)]
for i in range(line_count):
    for j in range(i+1):
        dist_matrix[i][j] = 1-SI(seqs[i],seqs[j])
        dist_matrix[j][i] = 1-SI(seqs[i],seqs[j])
# Distance matrix made successfully at this point
dm3 = dist_matrix
print("dm3", dm3)
dm = DistanceMatrix(dist_matrix, dates)
# print(len(dist_matrix[0]))




##below two lines shou.d be uncommented later
# dates = ['a','b', 'c', 'd','e']
# dm = DistanceMatrix(dm3, dates)
newick_str = nj(dm, result_constructor=str)
print(newick_str)
tree = nj(dm) # make tree using inbuild nj from skbio
print(tree.ascii_art()) # print tree
# dic = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4}
dic = {}
for i in range (len(dates)) :
    dic[dates[i]] = i
print("DICT :", dic )
G = skbio_tree_to_nx_graph(tree.root())
nodes = [node for node, degree in G.degree() if degree >= 1]
names = []
dist_mat = np.zeros((len(nodes), len(nodes)))
print("G has", G)
for i in range (len(nodes)) :
    names.append(nodes[i])
    for j in range (i+1,len(nodes)) :
        if (nodes[i] in dates and nodes[j] in dates) : 
            d = dm3[dic[nodes[i]]][dic[nodes[j]]]
            dist_mat[i][j] = dist_mat[j][i] = d
            G.add_edge(nodes[i], nodes[j], distance=d)
        # else :
        #     d = nx.shortest_path_length(G, nodes[i], nodes[j], weight='distance')
        #     dist_mat[i][j] = dist_mat[j][i] = d
        #     G.add_edge(nodes[i], nodes[j], distance=d)

print("G has", G)
for i in range (len(nodes)) :
    names.append(nodes[i])
    for j in range (i+1,len(nodes)) :
        if not (nodes[i] in dates and nodes[j] in dates) : 
            d = nx.shortest_path_length(G, nodes[i], nodes[j], weight='distance')
            dist_mat[i][j] = dist_mat[j][i] = d
            G.add_edge(nodes[i], nodes[j], distance=d)
print("G has", G)
print(dist_mat)
ste = mst_steiner(G, dates)
visualize_steiner_tree(ste,ste)
# write_dot(ste, "./out")
