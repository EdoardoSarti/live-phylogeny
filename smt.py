import networkx as nx
import matplotlib.pyplot as plt


def visualize_steiner_tree(steiner_tree, graph):
    pos = nx.spring_layout(graph)  # Layout for node positioning
    edge_labels = nx.get_edge_attributes(steiner_tree, 'weight')  # Get edge weights as labels
    
    nx.draw_networkx(graph, pos, with_labels=True, node_color='lightblue', node_size=500, edge_color='gray')
    nx.draw_networkx_edges(steiner_tree, pos, edgelist=steiner_tree.edges(), edge_color='red', width=2.0, alpha=0.5)
    nx.draw_networkx_edge_labels(steiner_tree, pos, edge_labels=edge_labels)  # Display edge labels
    plt.title("Steiner Tree")
    plt.show()

def mst_steiner(graph, terminals):
    # Step 1: Construct the metric closure on the terminal set
    metric_closure = nx.Graph()
    # edges = nx.get_edge_attributes(graph, "weight")
    # print(edges)
    # print(edges[("a","b")])

    for terminal1 in terminals:
        for terminal2 in terminals:
            if terminal1 != terminal2:
                shortest_path = nx.shortest_path(graph, terminal1, terminal2, weight='distance')

                path_length = nx.shortest_path_length(graph, terminal1, terminal2, weight='distance')
                print(path_length)
                metric_closure.add_edge(terminal1, terminal2, weight=path_length)
    
    # Step 2: Find an MST on the metric closure
    mst = nx.minimum_spanning_tree(metric_closure)
    visualize_steiner_tree(mst,metric_closure)
    # Step 3: Initialize the Steiner tree
    steiner_tree = nx.Graph()
    
    # Step 4: Traverse the MST edges in a depth-first-search order
    print("***** DFS MANNER ITERATION STARTS ****")
    dfs_edges = nx.dfs_edges(mst)
    for edge in dfs_edges:
        print()
        u, v = edge
        print("Edge :", u, v)
        # Step 4.1: Find a shortest path from u to v in the original graph
        shortest_path = nx.shortest_path(graph, u, v, weight='distance')
        print("SHORTEST PATH:", shortest_path)
        print("TREE NODES:", steiner_tree.nodes())
        all_shortest_path = nx.all_shortest_paths(graph, u, v, weight='distance')
        long_path = shortest_path
        for path in all_shortest_path :
            if ("emp1" in path) or ("emp2" in path) or ("emp3" in path) :
                if len(path) > len(long_path) :
                    long_path = path
                print(path)
        # print(all_shortest_path)
        shortest_path = long_path
        # Step 4.2: Add the path to the Steiner tree
        if len(set(shortest_path) & set(steiner_tree.nodes())) < 100:
            # Add the entire path if it has less than two vertices in the Steiner tree
            steiner_tree.add_edges_from(nx.utils.pairwise(shortest_path))
            # visualize_steiner_tree(steiner_tree,steiner_tree)

            print("HERE",steiner_tree)

        else:
            # Otherwise, find the first and last vertices in the Steiner tree
            pi = next(filter(lambda node: node in steiner_tree.nodes(), shortest_path))
            pj = next(filter(lambda node: node in steiner_tree.nodes(), reversed(shortest_path)))
            
            # Add subpaths from u to pi and from pj to v
            pi_to_pj_path = shortest_path[shortest_path.index(pi):shortest_path.index(pj)+1]
            steiner_tree.add_edges_from(nx.utils.pairwise(pi_to_pj_path))
            print("THERE",steiner_tree)
    
    # Step 5: Return the Steiner tree
    return steiner_tree