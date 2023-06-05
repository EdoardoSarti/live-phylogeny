from treeGen import *
import networkx as nx
from smt import *
import matplotlib.pyplot as plt

def visualize_steiner_tree(steiner_tree, graph):
    pos = nx.spring_layout(graph)  # Layout for node positioning
    edge_labels = nx.get_edge_attributes(steiner_tree, 'weight')  # Get edge weights as labels
    
    nx.draw_networkx(graph, pos, with_labels=True, node_color='lightblue', node_size=500, edge_color='gray')
    nx.draw_networkx_edges(steiner_tree, pos, edgelist=steiner_tree.edges(), edge_color='red', width=2.0, alpha=0.5)
    nx.draw_networkx_edge_labels(steiner_tree, pos, edge_labels=edge_labels)  # Display edge labels
    plt.title("Steiner Tree")
    plt.show()
dm2 = [[0,4,3,1,4,4,6,3,1,2,2],[4,0,3,5,4,4,10,7,3,2,6],[3,3,0,4,1,1,9,6,2,1,5],[1,5,4,0,5,5,7,4,2,3,3],[4,4,1,5,0,2,10,7,3,2,5],[4,4,1,5,2,0,10,7,3,2,5],[6,10,9,7,10,10,0,5,7,8,4],[3,7,6,4,7,7,5,0,4,5,1],[1,3,2,2,3,3,7,4,0,1,3],[2,2,1,3,2,2,8,5,1,0,4],[2,6,5,3,5,5,4,1,3,4,0]]
D2 = {"a" : 0, "b" : 1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7, "emp1":8, "emp2":9, "emp3":10}

print(dm)
D = {"emp3" : 0, "emp2" : 1, "a":2, "b":3, "c":4, "d":5, "emp1":6, "e":7, "f":8, "g":9, "h":10}
# dm[D["e"]][D["f"]] = 100
# dm[D["f"]][D["e"]] = 100
G = nx.Graph()
G.add_node("b")
G.add_node("e")
G.add_node("f")
G.add_node("c")
G.add_node("emp2")
G.add_node("d")
G.add_node("g")
G.add_node("h")
G.add_node("emp1")
G.add_node("a")
G.add_node("emp3")
# for i in range (11) : 
#     G.add_node(D[i])
for node1 in G :
    for node2 in G :
        G.add_edge(node1, node2, distance=dm2[D2[node1]][D2[node2]])
        # print(node1,node2)
print(G)
steiner_tree=mst_steiner(G, ["e", "b", "f", "c", "d", "g", "h", "a"])
visualize_steiner_tree(steiner_tree, G)


# D1 = {"a" : 0, "b" : 1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
# G1 = nx.Graph()
# G1.add_node("a")
# G1.add_node("b")
# G1.add_node("c")
# G1.add_node("d")
# G1.add_node("e")
# G1.add_node("f")
# G1.add_node("g")
# G1.add_node("h")
# dm1 = [[0,4,3,1,4,4,6,3],[4,0,3,5,4,4,10,7],[3,3,0,4,1,1,9,6],[1,5,4,0,5,5,7,4],[4,4,1,5,0,2,10,7],[4,4,1,5,2,0,10,7],[6,10,9,7,10,10,0,5],[3,7,6,4,7,7,5,0]]

# for node1 in G1:
#     for node2 in G1 :
#         G1.add_edge(node1, node2, distance=dm1[D1[node1]][D1[node2]])
#         # print(node1,node2)
# # print(G1)
# print("**************** STEINER_MIX OVER ******************")
# steiner_tree1=mst_steiner(G1, ["a", "b", "c", "d", "e", "f", "g", "h"])
# visualize_steiner_tree(steiner_tree1, G1)





