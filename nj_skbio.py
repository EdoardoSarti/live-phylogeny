import numpy as np
from six import StringIO

from skbio.stats.distance import DistanceMatrix
from skbio.tree import TreeNode
import matplotlib.pyplot as plt
# from usage2 import dist_mat
from sklearn.manifold import MDS


def nj(dm, disallow_negative_branch_length=True, result_constructor=None):

    if dm.shape[0] < 3:
        raise ValueError(
            "Distance matrix must be at least 3x3 to "
            "generate a neighbor joining tree.")

    if result_constructor is None:
        result_constructor = \
            lambda x: TreeNode.read(StringIO(x), format='newick')

    # initialize variables
    node_definition = None

    # while there are still more than three distances in the distance matrix,
    # join neighboring nodes.
    while(dm.shape[0] > 3):
        mds = MDS(n_components=2, dissimilarity='precomputed')
        coordinates = mds.fit_transform(dm.data)


        # colors = ['red' if i in datanodes else 'blue' for i in range(coordinates.shape[0])]

        plt.scatter(coordinates[:, 0], coordinates[:, 1])
        # plt.scatter(coordinates[:, 0], coordinates[:, 1], c=colors)

        plt.show()

        # compute the Q matrix
        q = _compute_q(dm)

        # identify the pair of nodes that have the lowest Q value. if multiple
        # pairs have equally low Q values, the first pair identified (closest
        # to the top-left of the matrix) will be chosen. these will be joined
        # in the current node.
        idx1, idx2 = _lowest_index(q)
        pair_member_1 = dm.ids[idx1]
        pair_member_2 = dm.ids[idx2]
        # determine the distance of each node to the new node connecting them.
        pair_member_1_len, pair_member_2_len = _pair_members_to_new_node(
            dm, idx1, idx2, disallow_negative_branch_length)
        # define the new node in newick style
        node_definition = "(%s:%f, %s:%f)" % (pair_member_1,
                                              pair_member_1_len,
                                              pair_member_2,
                                              pair_member_2_len)
        # compute the new distance matrix, which will contain distances of all
        # other nodes to this new node
        dm = _compute_collapsed_dm(
            dm, pair_member_1, pair_member_2,
            disallow_negative_branch_length=disallow_negative_branch_length,
            new_node_id=node_definition)

    # When there are three distances left in the distance matrix, we have a
    # fully defined tree. The last node is internal, and its distances are
    # defined by these last three values.
    # First determine the distance between the last two nodes to be joined in
    # a pair...
    pair_member_1 = dm.ids[1]
    pair_member_2 = dm.ids[2]
    pair_member_1_len, pair_member_2_len = \
        _pair_members_to_new_node(dm, pair_member_1, pair_member_2,
                                  disallow_negative_branch_length)
    # ...then determine their distance to the other remaining node, but first
    # handle the trival case where the input dm was only 3 x 3
    node_definition = node_definition or dm.ids[0]
    internal_len = _otu_to_new_node(
        dm, pair_member_1, pair_member_2, node_definition,
        disallow_negative_branch_length=disallow_negative_branch_length)
    # ...and finally create the newick string describing the whole tree.
    newick = "(%s:%f, %s:%f, %s:%f);" % (pair_member_1, pair_member_1_len,
                                         node_definition, internal_len,
                                         pair_member_2, pair_member_2_len)

    # package the result as requested by the user and return it.
    return result_constructor(newick)


def _compute_q(dm):
    q = np.zeros(dm.shape)
    n = dm.shape[0]
    for i in range(n):
        for j in range(i):
            q[i, j] = q[j, i] = \
                ((n - 2) * dm[i, j]) - dm[i].sum() - dm[j].sum()
    return DistanceMatrix(q, dm.ids)


def _compute_collapsed_dm(dm, i, j, disallow_negative_branch_length,
                          new_node_id):
    in_n = dm.shape[0]
    out_n = in_n - 1
    out_ids = [new_node_id]
    out_ids.extend([e for e in dm.ids if e not in (i, j)])
    result = np.zeros((out_n, out_n))
    for idx1, out_id1 in enumerate(out_ids[1:]):
        result[0, idx1 + 1] = result[idx1 + 1, 0] = _otu_to_new_node(
            dm, i, j, out_id1, disallow_negative_branch_length)
        for idx2, out_id2 in enumerate(out_ids[1:idx1+1]):
            result[idx1+1, idx2+1] = result[idx2+1, idx1+1] = \
                dm[out_id1, out_id2]
    return DistanceMatrix(result, out_ids)


def _lowest_index(dm):
    lowest_value = np.inf
    for i in range(dm.shape[0]):
        for j in range(i):
            curr_index = i, j
            curr_value = dm[curr_index]
            if curr_value < lowest_value:
                lowest_value = curr_value
                result = curr_index
    return result


def _otu_to_new_node(dm, i, j, k, disallow_negative_branch_length):
    k_to_u = 0.5 * (dm[i, k] + dm[j, k] - dm[i, j])
    if disallow_negative_branch_length and k_to_u < 0:
        k_to_u = 0
    return k_to_u


def _pair_members_to_new_node(dm, i, j, disallow_negative_branch_length):
    n = dm.shape[0]
    i_to_j = dm[i, j]
    i_to_u = (0.5 * i_to_j) + ((dm[i].sum() - dm[j].sum()) / (2 * (n - 2)))

    if disallow_negative_branch_length and i_to_u < 0:
        i_to_u = 0

    j_to_u = i_to_j - i_to_u

    if disallow_negative_branch_length and j_to_u < 0:
        j_to_u = 0

    return i_to_u, j_to_u