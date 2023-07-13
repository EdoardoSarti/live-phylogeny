from skbio.tree import TreeNode
from skbio import DistanceMatrix
from usage import tree
import skbio.tree 

# "tree" is the skbio tree obtained by applying NJ on the Distance Matrix
def printL(l) : 
    for x in l : print(x.name)
def printP(l) : 
    for (u,v) in l : print(u.name, v.name)

L = []
for x in tree.tips() : 
    L.append(x)
print("ORIGINAL TREE:")
print(tree.ascii_art())
count = 1
pairs = []
while (len(L)>2 and count < 10) : 
    print("######## ITERATION " + str(count) + " #########")
    count += 1
    pairs = []
    for i in range (len(L)) : 
        for j in range (i+1,len(L)) : 
            if (L[i].parent==L[j].parent) : 
                pairs.append((L[i],L[j]))
    print("L is : ")
    printL(L)
    print()
    print("Pairs are:")
    printP(pairs)
    print()
    for (u,v) in pairs :
        print("parent:", u.parent.name)
        print("children:")
        L.remove(u)
        L.remove(v)
        d1 = u.distance(u.parent)
        d2 = v.distance(v.parent)
        print("d1 and d2 ", d1, d2)
        if (d1 > 1.5*d2) : 
            d3 = u.parent.length
            u.parent = v
            v.children.append(u)
            if v.parent.parent is not None :
                v.length = d3
                v.parent.parent.children.append(v)
                v.parent.parent.children.remove(v.parent)
                v.parent = v.parent.parent
            else : v.parent = v.parent.parent
            print("u.name", u.name)
            print("v.name", v.name)
            print("u.parent", u.parent)
            print()
            L.append(v)
        elif (d2 > 1.5*d1):
            d3 = v.parent.length
            v.parent = u
            u.children.append(v)
            if u.parent.parent is not None :
                u.length = d3
                u.parent.parent.children.append(u)
                u.parent.parent.children.remove(u.parent)
                u.parent = u.parent.parent
            else : u.parent = u.parent.parent
            print("u.name", u.name)
            print("v.name", v.name)
            print("u.parent", u.parent)
            print()
            L.append(u)
        else :
            L.append(u.parent)
    print(tree.ascii_art()) # print tree
    # tree2 = tree.root_at(tree.find("ancestor"))
    # print(tree2.ascii_art())
    print()
    print()
    





# import networkx as nx

# G = nx.Graph()

# # def check(L) : # L is the list of nodes, if it contains 
# #     for x in L :
# #         if "_" in L : return False
# #     return True

# def modifyG(G) : 