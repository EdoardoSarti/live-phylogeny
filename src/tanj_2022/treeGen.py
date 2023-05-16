from ete3 import Tree
import numpy as np

topol = "((d)a,((e,f)b,c)INT1)INT2;"

# topol = "((((a,(c,d)INT1)b)e)f,(((l,m)h)g,((k)j)i)INT2)INT3;"
t = Tree(topol, format=8)

nl = 0
for n in t.traverse():
    if (n.name[:3]=="INT"):
        continue
    n.add_feature("dist",np.random.uniform()+1)
    nl += 1

        
noise= np.zeros((nl,nl))
for i in range (nl):
    for j in range(i+1,nl):
        r= 1*np.random.randn() + 0
        noise[i][j]=noise[j][i]=r

print(t.get_ascii(attributes=["name","dist"],show_internal=True))

labels = []
dm = -np.ones((nl, nl))
in1, in2 = -1, -1
for n1 in t.traverse():
    if (n1.name[:3]=="INT"):
        continue 
    in1 += 1
    labels.append(n1.name)
    in2 = -1
    for n2 in t.traverse():
        if (n2.name[:3]=="INT"):
            continue
        in2 += 1
        dm[in1, in2] = n1.get_distance(n2)


dmnoisy= 0.1*noise*dm+dm

print(dm)

print(dmnoisy)
