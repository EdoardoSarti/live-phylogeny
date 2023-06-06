import networkx as nx
import matplotlib.pyplot as plt

def visualize_steiner_tree(steiner_tree, graph):
    pos = nx.spring_layout(graph)  # Layout for node positioning
    edge_labels = nx.get_edge_attributes(steiner_tree, 'weight')  # Get edge weights as labels
    res = {key : round(edge_labels[key], 2) for key in edge_labels}
    nx.draw_networkx(graph, pos, with_labels=True, node_color='lightblue', node_size=500, edge_color='gray')
    nx.draw_networkx_edges(steiner_tree, pos, edgelist=steiner_tree.edges(), edge_color='red', width=2.0, alpha=0.5)
    nx.draw_networkx_edge_labels(steiner_tree, pos, edge_labels=res)  # Display edge labels
    plt.title("Steiner Tree")
    plt.show()

def mst_steiner(graph, terminals):
    print("CHECK GRAPH", graph)
    # Step 1: Construct the metric closure on the terminal set
    metric_closure = nx.Graph()

    for terminal1 in terminals:
        for terminal2 in terminals:
            if terminal1 != terminal2:
                shortest_path = nx.shortest_path(graph, terminal1, terminal2, weight='distance')
                path_length = nx.shortest_path_length(graph, terminal1, terminal2, weight='distance')
                metric_closure.add_edge(terminal1, terminal2, weight=path_length)
    
    # Step 2: Find an MST on the metric closure
    mst = nx.minimum_spanning_tree(metric_closure)
    visualize_steiner_tree(mst,metric_closure)

    # Step 3: Initialize the Steiner tree
    steiner_tree = nx.Graph()
    
    # Step 4: Traverse the MST edges in a depth-first-search order
    dfs_edges = nx.dfs_edges(mst)
    for edge in dfs_edges:
        u, v = edge
        # Step 4.1: Find a shortest path from u to v in the original graph
        shortest_path = nx.shortest_path(graph, u, v, weight='distance')
        all_shortest_path = nx.all_shortest_paths(graph, u, v, weight='distance')
        long_path = shortest_path
        for path in all_shortest_path :
            if len(path) > len(long_path) :
                long_path = path
        shortest_path = long_path

        # Step 4.2: Add the path to the Steiner tree
        if len(set(shortest_path) & set(steiner_tree.nodes())) < 2:
            # Add the entire path if it has less than two vertices in the Steiner tree
            for i in range (0,len(shortest_path)-1) : 
                path_length = nx.shortest_path_length(graph, shortest_path[i], shortest_path[i+1], weight='distance')
                steiner_tree.add_edge(shortest_path[i],shortest_path[i+1], weight = path_length)
        else:
            # Otherwise, find the first and last vertices in the Steiner tree
            pi = next(filter(lambda node: node in steiner_tree.nodes(), shortest_path))
            pj = next(filter(lambda node: node in steiner_tree.nodes(), reversed(shortest_path)))
            # Add subpaths from u to pi and from pj to v
            pi_path = shortest_path[:shortest_path.index(pi)]
            pj_path = shortest_path[shortest_path.index(pj):]
            for i in range (0,len(pi_path)-1) : 
                path_length = nx.shortest_path_length(graph, pi_path[i], pi_path[i+1], weight='distance')
                steiner_tree.add_edge(pi_path[i],pi_path[i+1], weight = path_length)
            for i in range (0,len(pj_path)-1) : 
                path_length = nx.shortest_path_length(graph, pj_path[i], pj_path[i+1], weight='distance')
                steiner_tree.add_edge(pj_path[i],pj_path[i+1], weight = path_length)
    
    # Step 5: Return the Steiner tree
    return steiner_tree
