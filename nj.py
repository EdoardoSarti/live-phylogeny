from skbio import DistanceMatrix
from skbio.tree import nj
import networkx as nx

def skbio_tree_to_nx_graph(tree):
    graph = nx.Graph()

    def traverse(node):
        if node is None:
            return

        print("Node", node.name, node.children)
        counter = 0
        for child in node.children:
            if child.name is None:
                child.name = node.name + '_' + str(counter)
                counter += 1
            graph.add_node(child.name)
            graph.add_edge(node.name, child.name, distance=node.distance(child))
            traverse(child)
    tree.root().name = 'r'
    graph.add_node(tree.root().name)
    traverse(tree.root())
    print("TREE TO GRAPH:", graph)

    return graph