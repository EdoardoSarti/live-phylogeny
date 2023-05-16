import gnj
import dataGen
import numpy as np
def GNJ_test():
    distmat= np.load("/user/ragupta/home/time-aware-neighbor-joining/data/distMat.npy")
    
    labels=dataGen.labels
    t= gnj.GeneralizedNJ(distmat,labels)
    print(" Done...Hopefully :') ")
if __name__ == "__main__":
    GNJ_test()