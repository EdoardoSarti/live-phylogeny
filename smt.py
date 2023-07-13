import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from networkx.drawing.nx_agraph import write_dot
import networkx as nx


def visualize_steiner_tree(steiner_tree, graph):
    pos = nx.nx_agraph.graphviz_layout(graph, prog='dot')  # Reingold-Tilford Tree layout
    edge_labels = nx.get_edge_attributes(steiner_tree, 'weight')  # Get edge weights as labels
    res = {key : round(edge_labels[key], 2) for key in edge_labels}
    nx.draw_networkx(graph, pos, with_labels=True, node_color='lightblue', node_size=500, edge_color='gray')
    nx.draw_networkx_edges(steiner_tree, pos, edgelist=steiner_tree.edges(), edge_color='red', width=2.0, alpha=0.5)
    nx.draw_networkx_edge_labels(steiner_tree, pos, edge_labels=res)  # Display edge labels
    plt.title("Steiner Tree")
    plt.show()

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


def second_shortest_path(graph, source, target):
    shortest_path = nx.shortest_path(graph, source, target, weight='weight')
    shortest_path_length = nx.shortest_path_length(graph, source, target, weight='weight')
    print("Shortest path length", shortest_path_length)
    second_shortest_path = []
    second_shortest_path_length = 0
    for i in range (len(shortest_path)-1) :
        print("Try Removing",shortest_path[i], shortest_path[i+1])
        # print(type(e))
        path_length = nx.shortest_path_length(graph, shortest_path[i], shortest_path[i+1], weight='weight')
        graph.remove_edge(shortest_path[i], shortest_path[i+1])
        ssp = nx.shortest_path(graph, source, target, weight='weight')
        print("Tried path", ssp)
        if not checkNoTerminals(ssp) : continue
            # for ii in range (len(ssp)-1) :
            #     pl = nx.shortest_path_length(graph, ssp[ii], ssp[ii+1], weight='weight')
            #     graph.remove_edge(ssp[ii], ssp[ii+1])
            #     ssp = nx.shortest_path(graph, source, target, weight='weight')
            #     graph.add_edge(ssp[ii],ssp[ii+1], weight = pl)
            #     if checkNoTerminals(ssp) : return pl/shortest_path_length, ssp, pl
        sspl = nx.shortest_path_length(graph, source, target, weight='weight')
        print("sspl", sspl)
        if second_shortest_path == [] or sspl < second_shortest_path_length: 
            second_shortest_path = ssp
            second_shortest_path_length = sspl
        graph.add_edge(shortest_path[i],shortest_path[i+1], weight = path_length)
        # visualize_steiner_tree(graph,graph)

    # graph.remove_edges_from(zip(shortest_path, shortest_path[1:]))
    # second_shortest_path = nx.shortest_path(graph, source, target, weight='distance')
    # graph.add_edges_from(zip(shortest_path, shortest_path[1:]))

    # second_shortest_path_length = nx.shortest_path_length(graph, source, target, weight='distance')
    r = second_shortest_path_length/shortest_path_length
    if second_shortest_path == [] : return 2, [], 0
    return r, second_shortest_path, second_shortest_path_length

def checkNoTerminals(l) : 
    if len(l)<=2 : return True
    else :
        for i in range (1, len(l)-1) : 
            if "|" in l[i] : return False
    return True

def mst_steiner(graph, terminals, leavesdict):
    print("Graph desc:", graph)
    print("Terminals :", terminals)
    print("leavesdict :", leavesdict)
    # Construct the metric closure on the terminal set
    metric_closure = nx.Graph()

    for terminal1 in terminals:
        for terminal2 in terminals:
            if terminal1 != terminal2:
                # shortest_path = nx.shortest_path(graph, terminal1, terminal2, weight='distance')
                # print(shortest_path)
                # path_length = nx.shortest_path_length(graph, terminal1, terminal2, weight='distance')
                path_length = 1-SI(leavesdict[terminal1],leavesdict[terminal2])
                metric_closure.add_edge(terminal1, terminal2, weight=path_length)
    
    # Find an MST on the metric closure
    mst = nx.minimum_spanning_tree(metric_closure)
    # visualize_steiner_tree(metric_closure,metric_closure)
    visualize_steiner_tree(graph,graph)
    print("GRAPH PRINTED")
    print([node for node, degree in graph.degree() if degree >= 1])
    visualize_steiner_tree(mst,mst)
    write_dot(mst, "./givenTree.dot")
    # visualize_steiner_tree(mst,metric_closure)

    # Initialize the Steiner tree
    steiner_tree = nx.Graph()
    
    # Traverse the MST edges in a depth-first-search order
    dfs_edges = nx.dfs_edges(mst)
    for edge in dfs_edges:
        u, v = edge
        print("EDGES:", u, v)
        # Find a shortest path from u to v in the original graph
        
        

        shortest_path = nx.shortest_path(graph, u, v, weight='weight')
        all_shortest_path = nx.all_shortest_paths(graph, u, v, weight='weight')
        long_path = shortest_path
        for path in all_shortest_path :
            print("Possible path:", path)
            if len(path) > len(long_path) :
                long_path = path
        shortest_path = long_path


        # Uncomment 5 lines below to allow for some tolerance to the path between two adjecent vertices
        # shortest_path = nx.shortest_path(graph, u, v, weight='weight')
        # a,b,c = second_shortest_path(graph, u, v)
        # print(a)
        # if a<1.35 : shortest_path = b
        # print("Shortest Path :", shortest_path)


        # Add the path to the Steiner tree
        if len(set(shortest_path) & set(steiner_tree.nodes())) < 2:
            # Add the entire path if it has less than two vertices in the Steiner tree
            for i in range (0,len(shortest_path)-1) : 
                path_length = nx.shortest_path_length(graph, shortest_path[i], shortest_path[i+1], weight='weight')
                steiner_tree.add_edge(shortest_path[i],shortest_path[i+1], weight = path_length)
        else:
            # Otherwise, find the first and last vertices in the Steiner tree
            pi = next(filter(lambda node: node in steiner_tree.nodes(), shortest_path))
            pj = next(filter(lambda node: node in steiner_tree.nodes(), reversed(shortest_path)))
            # Add subpaths from u to pi and from pj to v
            pi_path = shortest_path[:shortest_path.index(pi)]
            pj_path = shortest_path[shortest_path.index(pj):]
            for i in range (0,len(pi_path)-1) : 
                path_length = nx.shortest_path_length(graph, pi_path[i], pi_path[i+1], weight='weight')
                steiner_tree.add_edge(pi_path[i],pi_path[i+1], weight = path_length)
            for i in range (0,len(pj_path)-1) : 
                path_length = nx.shortest_path_length(graph, pj_path[i], pj_path[i+1], weight='weight')
                steiner_tree.add_edge(pj_path[i],pj_path[i+1], weight = path_length)
        print(steiner_tree.nodes())
        print()

    # Return the Steiner tree
    return steiner_tree
