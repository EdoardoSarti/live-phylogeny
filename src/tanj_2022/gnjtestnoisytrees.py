import gnj2
import gnj2NJForced
import treeGen
import numpy as np
def GNJ_test():
    # distmat= np.load("/user/ragupta/home/time-aware-neighbor-joining/data/distMat.npy")
    # distmat= np.load("/user/ragupta/home/time-aware-neighbor-joining/data/distMatupdated.npy")

    # distmat= np.load("/user/ragupta/home/time-aware-neighbor-joining/data/distMattimedissected.npy")

    # distmat= np.load("/user/ragupta/home/time-aware-neighbor-joining/data/distMatSynthSeqs.npy")
    distmat= treeGen.dm
    distmat1= distmat.copy()
    distmatNoisy= treeGen.dmnoisy
    distmat2= distmatNoisy.copy()

    # distmat=np.subtract(distmat,np.identity(distmat.shape[0]))
    # labels=dataGen.labels
    # labels=dataGenSynthSeqs.labels
    
    labels=treeGen.labels

    labels1= labels.copy()
    labels2= labels.copy()
    labels3= labels.copy()
    print(len(labels))
    
    print(distmat.shape)
    print("---EXACT TANJ---")
    t= gnj2.GeneralizedNJ(distmat,labels)
    # labels1=treeGen.labels
    print(len(labels1))

    print("---NOISY TANJ---")
    gnj2.GeneralizedNJ(distmatNoisy,labels1)
    
    print("---EXACT NJ---")
    gnj2NJForced.GeneralizedNJ(distmat1,labels2)
    print("---NOISY NJ---")
    gnj2NJForced.GeneralizedNJ(distmat2,labels3)
    
    print(" Done...Hopefully :') ")
    

if __name__ == "__main__":
    GNJ_test()
