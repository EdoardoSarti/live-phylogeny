from GNJ_matrices2 import *
# from GNJ_matrices3 import *

import time
#ix the tree at the last step(observe gnj mat and bnj mat and tree with distances for the eact four case and youll know what to do)
# import treeGen
def GeneralizedNJ(d,labels):
    #Add function to check if matrix is symmetric


    
    dis=np.array(d)
    t= Tree()
    labels1= labels.copy() 
    for x in labels1:
        temp=t.add_child(name=x)

    matobj= GNJmat(dis,labels,t)
    # print(matobj.modmatgen())
    # print(vars(matobj))
    # # print(matobj.GNJpart)
    def fnc1(i,j):
        r= np.shape(matobj.DistMat)[0]

        return 0.5*matobj.DistMat[i][j] - (matobj.distsums[i]+ matobj.distsums[j])/(2*(r-2))
    def fnc2(i,j):
        r= np.shape(matobj.DistMat)[0]

    #     return matobj.GNJpart[i][j] - matobj.distsums[i]/(r-2)
    its=0
    cnt=0
    bnjsteps=0
    gnjsteps=0
    start1= time.perf_counter()
    # file1= open('/user/ragupta/home/time-aware-neighbor-joining/data/progress.txt','w')
    while(np.shape(matobj.DistMat)[0]>2):
        start = time.perf_counter()
        cnt+=1
        # file1.write("iteration: "+ str(cnt)+"\n" )
        print("iteration: "+ str(cnt) )
        matobj.giveQ(fnc1,fnc2)
        #uncomment following lines to see at each step
        # print("Qbnj:")
        # print(matobj.Qbnj)
        # print("Qgnj:")
        # print(matobj.Qgnj)

        # #giving preference to gnj
        print("qminbnj: " + str(matobj.qminBnj))
        print("qminGnj: " + str(matobj.dminGnj))
        print("difference: "+ str(matobj.qminBnj-matobj.dminGnj))

        if(matobj.dminGnj<matobj.qminBnj or abs(matobj.dminGnj- matobj.qminBnj)<= 0):
            matobj.update(matobj.iminGNJ,matobj.jminGNJ,0,its)
            gnjsteps+=1
            print("Imposing GNJ")        
        else:
            its+=1
            matobj.update(matobj.iminBNJ,matobj.jminBNJ,1,its)
            bnjsteps+=1
            print("imposing BNJ")

        #uncomment following lines to see at each step
        # print("Now the tree looks like")
        # print(matobj.tr.get_ascii())
        # print("nj mat looks like:")
        # print(matobj.DistMat)
        # print(matobj.labelsNJ)
        # print("gnj part:")
        # print(matobj.GNJpart)
        # print(matobj.labelsGNJ)
        # print("node dictionary:")
        # print(matobj.nodeDict)

        end = time.perf_counter()
        
        # file1.write('labels NJ:'+str(matobj.labelsNJ.index('seq00607_20220305'))+'\n')
        
        # file1.write('labels GNJ:'+repr(matobj.labelsGNJ)+'\n')
        # file1.write("node dict: "+ repr(matobj.nodeDict['seq00607_20220305'])+'\n')
        print("time for iteration: "+ str(end-start))
        
        print("total time elapsed: "+ str(end-start1))
        print("BNJ steps: "+str(bnjsteps) +" GNJ Steps: "+ str(gnjsteps))
    matobj.tr.dist=0
    for c in matobj.tr.children:
        c.dist= matobj.DistMat[0][1]/2
    print("reducing tree")
    matobj.reduceTree()
    print(matobj.tr.get_ascii(attributes=["name","dist"],show_internal=True))
    # matobj.tr.write(format=1,outfile="/user/ragupta/home/time-aware-neighbor-joining/data/recreatedTree.nw")
    return matobj.tr.write()
    # return matobj.tr
# d = [
#         [0, 1 ,2, 3, 4],
#         [1, 0, 1, 2, 3],
#         [2, 1, 0, 1, 2],
#         [3, 2, 1, 0, 1],
#         [4, 3, 2, 1, 0]
#     ]
# labels = ['a', 'b', 'c', 'd', 'e']

# d = [
#         [  0,2.5,  7,8.7],
#         [2.5,  0,8.2,7.9],
#         [  7,8.2,  0,  8],
#         [8.7,7.9,  8,  0]
#     ]
# labels = ['a', 'b', 'c', 'd']
# d = [
#         [0, 1, 3, 1],
#         [1, 0, 1, 1],
#         [3, 1, 0, 1],
#         [1, 1, 1, 0]
#     ]
# labels = ['a', 'b', 'c', 'd']
# d = [
#     [0, 3, 7, 8],
#     [3, 0, 8, 9],
#     [7, 8, 0, 8],
#     [8, 9, 8, 0]
# ]
# labels = ['a', 'b', 'c', 'd']
# GeneralizedNJ(treeGen.dm,treeGen.labels)
# print(GeneralizedNJ(d,labels).get_ascii(attributes=['name','dist'],show_internal=True))
    
