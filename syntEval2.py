import random
import networkx as nx
import copy
from smt import *
from networkx.drawing.nx_agraph import write_dot

def evolve(s0) :
    s = copy.copy(s0)
    n = random.randint(1,10)
    for i in range (n):
        k = random.randint(0,99)
        if s[k] != "Z" : s[k] = chr(ord(s[k])+1)
        else : s[k] = "A"
    return s

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

alphabet = list("A B C D E F G H I J K L M N O P Q R S T U V W X Y Z".split())
LENGTH = 100   # Length of ancestoral sequence
G = nx.Graph()
ancestor = ancestor = random.choices(alphabet, k=LENGTH)
a = ancestor 
a = "r"
G.add_node(a)

print(''.join(ancestor), "ancestor")
def makeTree(n, a, branch) :
    if branch > 7 : return
    # print(n.name) 
    if random.random() < 0.75 : 
        x1 = evolve(a)
        branch += 1
        print(''.join(x1), n+"|"+"0")
        G.add_edge(n+"|"+"0", n)
        makeTree(n+"|"+"0", x1, branch + 1)

        x2 = evolve(a)
        branch += 1
        print(''.join(x2), n+"|"+"1")
        G.add_edge(n+"|"+"1", n)
        makeTree(n+"|"+"1", x2, branch +1)

nodecount = 0
branch = 0
makeTree(a, ancestor, 0)
visualize_steiner_tree(G,G)
write_dot(G,'./givenTree.dot')