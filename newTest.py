import numpy as np
from skbio import DistanceMatrix
from skbio.tree import nj
from smt import *
from nj import *

from treeGen import dmnoisy
nodeNames = list("b c d e f g h i j k l m n".split())
m = np.array(dmnoisy)
m = m[2:,2:]
dmnoisy = m
print(dmnoisy)
d_m = DistanceMatrix(dmnoisy, nodeNames)
newick_str = nj(d_m, result_constructor=str)
print(newick_str)
tree = nj(d_m) # make tree using inbuild nj from skbio
print(tree.ascii_art()) # print tree
gg = skbio_tree_to_nx_graph(tree)
visualize_steiner_tree(gg,gg)
