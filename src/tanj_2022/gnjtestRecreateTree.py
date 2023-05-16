import gnj2
import genTree
# import dataGen
# import dataGenSynthSeqs
# import dataGenTenPercent
import numpy as np
def GNJ_test():
    # distmat= np.load("/user/ragupta/home/time-aware-neighbor-joining/data/distMat.npy")
    # distmat= np.load("/user/ragupta/home/time-aware-neighbor-joining/data/distMatupdated.npy")

    # distmat= np.load("/user/ragupta/home/time-aware-neighbor-joining/data/distMattimedissected.npy")

    # distmat= np.load("/user/ragupta/home/time-aware-neighbor-joining/data/distMatSynthSeqs.npy")
    # distmat= genTree.dm

    distmat= np.load("/user/ragupta/home/time-aware-neighbor-joining/data/distMattreemetric.npy")
    
    # distmat=np.subtract(distmat,np.identity(distmat.shape[0]))
    # labels=dataGen.labels
    # labels=dataGenSynthSeqs.labels
    
    labels= genTree.labels
    print(distmat.shape)
    t= gnj2.GeneralizedNJ(distmat,labels)
    print(" Done...Hopefully :') ")
if __name__ == "__main__":
    GNJ_test()