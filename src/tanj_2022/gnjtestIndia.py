from math import dist
import gnj2
import datagenIndia
import numpy as np
def GNJ_test():
    # distmat= np.load("/user/ragupta/home/time-aware-neighbor-joining/data/distMat.npy")
    
    distmat= np.load("/user/ragupta/home/time-aware-neighbor-joining/data/IndiaUmapDistmat.npy")
    # distmat=np.subtract(distmat,np.identity(distmat.shape[0]))
    labels=datagenIndia.labels
    t= gnj2.GeneralizedNJ(distmat,labels)
    print(" Done...Hopefully :') ")
if __name__ == "__main__":
    GNJ_test()