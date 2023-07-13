import networkx as nx
from skbio import TreeNode

def build_tree(graph_dict):
    root_id = next(iter(graph_dict))
    root_node = TreeNode(name=str(root_id))

    stack = [(root_id, root_node)]

    while stack:
        node_id, node = stack.pop()
        children = graph_dict[node_id]
        for child_id in children:
            child_node = TreeNode(name=str(child_id))
            node.append(child_node)
            stack.append((child_id, child_node))

    return root_node

G = nx.Graph()
G.add_edges_from([(1, 2), (1, 3), (2, 4), (2, 5)])
graph_dict = nx.to_dict_of_lists(G)
print(G, graph_dict)
root_node = build_tree(graph_dict)
