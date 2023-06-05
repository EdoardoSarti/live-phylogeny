# live-phylogeny

### `smt.py` Cantains two functions 
- `visualize_steiner_tree` input : spanning tree (networkx graph) and the _backgroud_ graph, output : plot of tree
- `mst_steiner` input : networkx graph and a list of terminals, output : tree (networkx graph)

### `steinerMix.py` 
- uses the `mst_steiner` function from smt.py on a dummy example and visualises using `visualize_steiner_tree`
