import networkx as nx
import matplotlib.pyplot as plt
from smt import *
import numpy as np
from nj import *
from skbio import DistanceMatrix
# from skbio.tree import nj
from nj_skbio import nj
from networkx.drawing.nx_agraph import write_dot

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

dm = DistanceMatrix(dist_matrix, dates)
newick_str = nj(dm, result_constructor=str)
print(newick_str)
tree = nj(dm) # make tree using inbuild nj from skbio
print(tree.ascii_art(show_internal = True)) # print tree



