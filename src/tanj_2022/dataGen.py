from supporting_functions import *
from tkinter import N
import numpy as np


f = open("../data/sel_L1273_noX_nordn_RBD.fasta", "r")
its=0
labels=[]
sequences=[]
months={}
for line in f:
    its+=1
    
    if(its%2):
        dt=line.split("|")[2]
        labels.append("seq"+str((its+1)//2).zfill(5)+"_"+dt.split("-")[0]+dt.split("-")[1]+dt.split("-")[2])
        if (dt.split("-")[1]+dt.split("-")[2]) in months:
            months[dt.split("-")[0]+dt.split("-")[1]].append((its+1)//2)
        else:
            months[dt.split("-")[0]+dt.split("-")[1]]=[(its+1)//2]
    else:
        sequences.append(line[:-1])
print(sorted(list(months.keys())))
labeltimedissected=[]

labelstimedissected=[]
np.random.seed(42)
for i in months.keys():
    temp=np.random.randint(len(months[i]))
    labelstimedissected.append(labels[months[i][temp]-1])
    labeltimedissected.append(months[i][temp])
# print((labelstimedissected))
# print(labels[0])    
# print(labels)
# print(len(sequences))
numbPoints=len(sequences)
distMat= np.zeros((numbPoints,numbPoints))
distMattimedissected=np.zeros((len(labeltimedissected),len(labeltimedissected)))
# distmat= np.load("/user/ragupta/home/time-aware-neighbor-joining/data/distMat.npy")
# distmat= 1-distmat
# print(distmat[0][0])
# np.save("/user/ragupta/home/time-aware-neighbor-joining/data/distMatupdated.npy",distmat)
#part below used for generating the distance matrix

for i in range( len(labeltimedissected)):
    for j in range(len(labeltimedissected)):
        distMattimedissected[i][j]=1-SI(sequences[labeltimedissected[i]-1],sequences[labeltimedissected[j]-1])
# print(distMattimedissected)
# np.save("/user/ragupta/home/time-aware-neighbor-joining/data/distMattimedissected.npy",distMattimedissected)

# with open('distMat.npy', 'wb') as f:
#     np.save(f,distMat)
