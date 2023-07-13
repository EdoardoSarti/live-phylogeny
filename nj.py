from skbio import DistanceMatrix
from skbio.tree import nj
import networkx as nx

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

def skbio_tree_to_nx_graph(tree):
    graph = nx.Graph()

    def traverse(node):
        if node is None:
            return

        counter = 0
        for child in node.children:
            if child.name is None:
                child.name = node.name + '_' + str(counter)
                counter += 1
            graph.add_node(child.name)
            d = node.distance(child)
            # Change the threshold and corresponding weight here
            if (d<=0.01) : graph.add_edge(node.name, child.name, weight=0.1)    
            else : 
                graph.add_edge(node.name, child.name, weight=d)
            traverse(child)
    tree.root().name = 'r'
    graph.add_node(tree.root().name)
    traverse(tree.root())

    return graph
