from supporting_functions import *
import numpy as np

f = open("../data/synthetic_sequences/synth_seqs.fasta", "r")
its=0
labels=[]
sequences=[]
for line in f:
    its+=1
    
    if(its%2):
        labels.append(line)
    else:
        # print(line)
        sequences.append(line)
numbPoints=len(sequences)
distMat= np.zeros((numbPoints,numbPoints))

for i in range(numbPoints):
    for j in range(numbPoints):
        distMat[i][j]=1-SI(sequences[i],sequences[j])
print(distMat)
np.save("../data/distMatSynthSeqs.npy",distMat)
