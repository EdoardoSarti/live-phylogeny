from unicodedata import name
from supporting_functions import *
import NJ
# import gnj
import gnj2NJForced

def NJ_tests():
    DMX_list = []  # List of distance matrices

    # Linear chain
    d = [
        [0, 1 ,2, 3, 4],
        [1, 0, 1, 2, 3],
        [2, 1, 0, 1, 2],
        [3, 2, 1, 0, 1],
        [4, 3, 2, 1, 0]
    ]
    labels = ['a', 'b', 'c', 'd', 'e']
    descr = "Linear chain"
    DMX_list.append((np.array(d), labels, descr))

    # Exact 4-leaf tree
    d = [
        [0, 3, 7, 8],
        [3, 0, 8, 9],
        [7, 8, 0, 8],
        [8, 9, 8, 0]
    ]
    labels = ['a', 'b', 'c', 'd']
    descr = "Exact 4-leaf tree"
    DMX_list.append((np.array(d), labels, descr))

    # Noisy 4-leaf tree
    d = [
        [  0,2.5,  7,8.7],
        [2.5,  0,8.2,7.9],
        [  7,8.2,  0,  8],
        [8.7,7.9,  8,  0]
    ]
    labels = ['a', 'b', 'c', 'd']
    descr = "Noisy 4-leaf tree"
    DMX_list.append((np.array(d), labels, descr))

    # 4-leaf tree not respecting triangular inequality
    d = [
        [0, 1, 3, 1],
        [1, 0, 1, 1],
        [3, 1, 0, 1],
        [1, 1, 1, 0]
    ]
    labels = ['a', 'b', 'c', 'd']
    descr = "4-leaf tree not respecting triangular inequality"
    DMX_list.append((np.array(d), labels, descr))

    for d, labels, descr in DMX_list:
        print(descr, NJ.triangularInequality(d))

        # Calculate tree using skbio
        nhx = tree.nj(DistanceMatrix(d, labels), result_constructor=str)
        t_truth = Tree(nhx)

        # Calculate tree using our implementation
        # t_test = gnj2NJForced.GeneralizedNJ(d,labels)#BasicNJ(d, labels)

        print("#"*30 + " " + descr)
        print(d)
        print("TRUTH")
        print(t_truth)
        print("TEST")
        # print(t_test.get_ascii(attributes=["name","dist"],show_internal=True))
        gnj2NJForced.GeneralizedNJ(d,labels)
        print("\n")

if __name__ == "__main__":
    NJ_tests()
