from cmath import inf
from os import rename
from platform import node
from tkinter.dialog import DIALOG_ICON
import numpy as np
from ete3 import Tree
class GNJmat:
    def __init__(self,DistMat,labels,tr) :
        self.DistMat = DistMat
        self.labelsNJ = labels
        # self.modmat = self.modmatgen()
        self.GNJpart= self.modmatgen()  #stores the GNJ part of the distance matrix        
        self.labelsGNJ = self.GNJlabelGen()
        self.nodeDict=self.genDict()
        self.numbnodes = np.shape(DistMat)[0] #initial number of nodes
        self.dminBnj= inf   #stores the current dmin of bnj
        self.dminGnj= inf    # similar
        self.qminBnj= inf
        self.Qbnj= None   #Q matrix of BNJ
        self.Qgnj= None   #similarlly
        self.iminBNJ= None  # current i index of the min value of Qbnj
        self.iminGNJ= None
        self.jminBNJ= None
        self.jminGNJ= None
        self.tr= tr
        
        self.distsums= self.distSum(self.DistMat)
    
    def GNJlabelGen(self):
        a=[]
        for i in self.labelsNJ:
            a.append(i+"1")
            a.append(i+"2")
        return a
    
    def genDict(self):#this dictionary will store the NJ nodes as the keys and the values as their children who can be in GNJ matrix and their distance fro this NJ node
        d={}
        for i in self.labelsNJ:
            d[i]=[[i+"1",0],[i+"2",0]]  
        return d
    
    def modmatgen(self):     #generates the initial GNJ matrix
        r= np.shape(self.DistMat)[0]
        d= np.zeros((r,2*r))
        for i in range(0,2*r,2):
            t=i//2
            d[:,i]= self.DistMat[:,t]
            d[:,i+1]= self.DistMat[:,t]
            
        return d
    
    
    def giveQ(self, q1,q2): 
        #returns the Q amtrix along with the first minimum values q1: func for calculating qij in BNJ and q2 for GNJ 
        # t is the tree (with the nodes storing the fact what children it has) 
        # add children list atribute using Node annotation in http://etetoolkit.org/docs/latest/tutorial/tutorial_trees.html#basic-tree-attributes
        r= np.shape(self.DistMat)[0]   #stores number of rows in the NJ dist mat
        dimGNJ = np.shape(self.GNJpart)   # stores dim of the GNJ mat 
        Qbnj= np.zeros(np.shape(self.DistMat))
        Qgnj= np.zeros(np.shape(self.GNJpart))
        iminBNJ= -inf
        jminBNJ=  -inf      
        dminBNJ= inf
        iminGNJ= -inf
        jminGNJ=  -inf      
        dminGNJ= inf
       
        vq1 = np.vectorize(q1)
        Qbnj = vq1(list(range(r)), list(range(r)))
        """
        for i in range(r):
            for j in range(i+1,r):
                #Qbnj[i][j] = q1(i,j)
                if (Qbnj[i][j] < dminBNJ):
                    dminBNJ=Qbnj[i][j]
                    iminBNJ=i
                    jminBNJ=j # will always be jmin > imin
        """
        imin = np.argmin(Qbnj.flatten())
        dminBNJ = Qbnj.flatten()[imin]
        iminBNJ = imin//r #CHECK
        jminBNJ = imin%r  #CHECK
        print("Done with Qbnj")
        
        #GNJ part
        for i in range(r):
            nameOfNJnode= self.labelsNJ[i]   #index of the row
            for k in self.nodeDict[nameOfNJnode]:  # finding the children of the node
                j=self.labelsGNJ.index(k[0]) #finding the child's index in the gnj label list
                Qgnj[i][j]=inf   #assigning that point the value of inf so as to prevent cyclization



        for i in range(dimGNJ[0]):
            for j in range(dimGNJ[1]):
                
                if(Qgnj[i][j]!=0): # if it is already a child then we must not consider it so as to prevent cycle formation
                    continue
                    
                Qgnj[i][j]=q2(i,j)   #here Q2 is the  function that will be used to alculate the q value
                if (Qgnj[i][j] < dminGNJ):
                    dminGNJ=Qgnj[i][j]
                    iminGNJ=i
                    jminGNJ=j # will always be jmin > imin
        print("Done with Q")
        self.dminBnj= dminBNJ*(2*(r-2))
        self.qminBnj= dminBNJ
        self.dminGnj= dminGNJ
        self.Qbnj= Qbnj
        self.Qgnj= Qgnj
        self.iminBNJ= iminBNJ
        self.iminGNJ= iminGNJ
        self.jminBNJ= jminBNJ
        self.jminGNJ= jminGNJ
    
    def distSum(self,A):
        print("distsumming")
        return np.sum(A, axis=1) #returns summmation(d(i,k))  {for each i, k ranges from 0 to r-1}
    
    
    def update(self,imin,jmin,bORg,its): 
        
        #updates the distance matrix as well as the tree and labels
        #imin and jmin are the selected indices and bORg is a bool deciding whether we need to impose the BNJ or GNJ 
        #its is the number of iterations
        tr= self.tr
        if(bORg): #assuming true means the bnj
            print("update BNJ")
            D0= self.DistMat.copy()
            r= np.shape(D0)[0]
            dfu= (self.dminBnj + 2*self.distsums[imin])/(2*(r-2))
            dgu= (self.dminBnj+ 2*self.distsums[jmin])/(2*(r-2))
            #note to self: use vectorisation to add and remove the f and g column and directly add the u column
            u= np.add(D0[imin],D0[jmin])/2- ((dfu+dgu)/2) #u th row
            #adding the uth row and column
            D0= np.r_[D0,[u]]
            # print(D0)
            print("BNJ move was calculated")

            u=np.append(u,0)
            # print(u)
            D0= np.c_[D0,u]
            F= tr&self.labelsNJ[imin]
            F_detached= F.detach()
            G= tr&self.labelsNJ[jmin]
            G_detached= G.detach()
            newname="("+self.labelsNJ[imin]+","+self.labelsNJ[jmin]+")IntNode"+str(its)
            self.labelsNJ.append(newname)  #creating label for the new node
            F_detached.dist = dfu
            G_detached.dist = dgu
            tmep= tr.add_child(name=newname)
            print("Tree structure was updated")
            # tmep.add_features(children=[])


            #!!!!!!!!!!!!!!!!!!!! Update the children list however you decide to implement it
            
            
            tmep.add_child(F_detached)
            tmep.add_child(G_detached)
            # tmep.children.append(F_detached.name)
            # tmep.children.append(G_detached.name)
            # tmep.children= tmep.children+ F_detached.children+ G_detached.children   #updating the list of children of the newly added node
            self.tr=tr
            
            #deleting the f g rows and columns from the distance matrix
            D0= np.delete(D0,imin,0)
            D0= np.delete(D0,jmin-1,0)
            D0= np.delete(D0,imin,1)
            D0= np.delete(D0,jmin-1,1)
            
            
            flabel= self.labelsNJ[imin]   #labels of the chosen nodes
            glabel = self.labelsNJ[jmin]
            
            self.labelsNJ.remove(self.labelsNJ[imin])
            self.labelsNJ.remove(self.labelsNJ[jmin-1])     #removing one node after one has been removed hence the -1
            
            
            
            #updating the dictionary
            for i in self.nodeDict[flabel]: #adding the distance dfu since the distance of allthe children in this will be dfu from u which will be added to the NJ matrix
                i[1]+=dfu
            for i in self.nodeDict[glabel]:
                i[1]+= dgu
            self.nodeDict[newname]= self.nodeDict[flabel]+ self.nodeDict[glabel] #taking union of both
            del self.nodeDict[flabel]
            del self.nodeDict[glabel] #deleting them as they are no longer part of the NJ
        
            
            
            #updating GNJ Matirx!


            D0_GNJ= self.GNJpart.copy()
            D0_GNJ= np.delete(D0_GNJ,imin,0)
            D0_GNJ= np.delete(D0_GNJ,jmin-1,0) #removing the ith and jth row from the gnj mat

            # ugnj= D0[-1][:self.numbnodes-2*its] # the first self.numbnodes-2*its of Distbnj and distgnj will be common as these are corresponding to the untouched nodes


    #i don't know if I really need the code below this :'(


            # ignj=-1
            # jgnj=-1
        
            # #seeing if the BNJ matrix has coloumns of the same label
            # for k in range(np.shape(D0_GNJ)[1]):
            #     if(self.labelsGNJ == flabel):
            #         ignj=k
            #     elif(self.labelsGNJ == glabel):
            #         jgnj= k
        
            # if(ignj>jgnj):
            #      jngj,ignj=ignj,jngj   #just in case ignj becomes greater than jgnj
        
            # if(ignj!=-1):
            #     F_GNJ= D0_GNJ[:][ignj]
            #     D0_GNJ= np.delete(D0_GNJ,ignj,1) #removing the already existing column of that node 
            #     D0_GNJ= np.c_[D0_GNJ,F_GNJ] #adding a zero column corresponding to the f node if it was already present in the gnj
            #     self.labelsGNJ.remove(flabel) #removing he label from the middle
            #     self.labelsGNJ.append(flabel) #adding it to the back
            # if(jgnj!=-1):
            #     if(ignj!=-1):
            #         jgnj-=1 #since we have already removed ignj and ignj<jgnj so jgnj shifts one unit to the left
            #     G_GNJ= D0_GNJ[:][jgnj]
            #     D0_GNJ= np.delete(D0_GNJ,jgnj,1) #removing the already existing column of that node 
            #     D0_GNJ= np.c_[D0_GNJ,G_GNJ] #adding a zero column corresponding to the g node if it was already present in the gnj
            #     self.labelsGNJ.remove(glabel) #removing the label from the middle
            #     self.labelsGNJ.append(glabel) #adding it to the back
        
    # :/

            for i in self.nodeDict[newname]: #so this step is becoming o(n^2) so ask if this is okay or if this could be optimized
                t= self.labelsGNJ.index(i[0]) #finding the index of the label of child in the labels list hence the current GNJ matrix
                # print("index is:"+str(t))
                # print(D0)

                # print(D0[:-1,-1])
                # print(D0[:-1,-1]+i[1])
                # print(D0_GNJ[:,t])

                # D0_GNJ[:,t]= D0[:-1,-1]+i[1] #adding the distance of the newnode(or u) with the appropriate constant distance of its child and updating the column of child's label 
                # print(D0_GNJ[:,t])
            #now i just have to add the last row to the gnj matrix
            # print("ehhehrer")
            # print(D0_GNJ)
            
            D0_GNJ= np.r_[ D0_GNJ, [np.zeros(np.shape(D0_GNJ)[1])]]
            # print("ehhehrer")
            # print(D0_GNJ)
            di=self.nodeDict.copy()
            for k,v in di.items(): #this step is o(n^3) i think but I cant think of a better way
                t= self.labelsNJ.index(k)
                temp= D0[-1][t]
                for i in v: 
                    t1= self.labelsGNJ.index(i[0]) 
                    # D0_GNJ[-1][t1]= D0[:-1][-1]+i[1] 

                    D0_GNJ[-1][t1]= temp + i[1] 
    
            self.DistMat=D0 #REMEMBER!!! note to self abhi meine mod mat update nahi kiya hai toh please karliyo rahul
            print("Matrix was updated")
            self.GNJpart=D0_GNJ
            self.distsums=self.distSum(self.DistMat)
            print("Distance vector sum was recalculated")

        
        else:   #upadating the tree and matrix in the case of GNJ aaagh
            #ask about if c goes to b then what will happen to the distances of the other nodes with b, should we change it like in bnj or keep it the same?
            print("update GNJ")
            glabel= self.labelsNJ[imin]  #stores the label of the selected node of the NJ matrix
            # lets suppose that node g is being detached and being attached to node f(note that g will be a part of the NJ nodes and f will be a GNJ node)
            flabel= self.labelsGNJ[jmin]
            #now we need to find the ky of f and its dstance from the key node to update distances of children of g
            dfparent=-1
            def findKey(dic,lab,dfparent):
                for k,v in dic.items():
                    for i in v:
                        if i[0]==lab:
                            dfparent=i[1]
                            return (k,dfparent)
            fparent,dfparent= findKey(self.nodeDict,flabel,dfparent) #stores label of parent of f and dist of f parent from g
            print("Parent found")
            
            dfg= self.GNJpart[imin][jmin] #stores distance between the f and g nodes
            # listOfChildren=  #stores the list of children of g and their distances from g
            
            #updating their distances

            for i in self.nodeDict[glabel]:
                i[1]+=(dfparent + dfg )            # now i can just add this to the children list of parent of f
            print("Dictionary updated")

            #the only change in the NJ matrix will be the rmoval of the ith row and column
            #change in the gnj will be the removal of g row and changes will be made to the children of the g node and f will be removed from the labels of gnj and column will also be removed
            #(although things might get organized if it is ossible not to delete the rows from the gnj distance matrix idk maybe not)
            #the tree alo need to be updated

            #updating the Tree
            tr= self.tr

            g= tr&self.labelsNJ[imin]
            g_detached = g.detach()

            fp= tr&self.labelsGNJ[jmin][:-1]    #[:-1] cuz placeholder be like A1 and we need A
            # fp= f.up
            # f= f.detach()
            g.dist= dfg

            fp.add_child(g)

            self.tr=tr
            print("Tree updated")


            #updating the NJ matrix
            D0 = self.DistMat.copy()
            D0 = np.delete(D0,imin,0)
            D0 = np.delete(D0,imin,1)

            self.labelsNJ.remove(self.labelsNJ[imin])

            self.nodeDict[fparent].remove([flabel,dfparent]) #removing the placeholder(hope it works idk:'))
            self.nodeDict[fparent]+= self.nodeDict[glabel] #taking union of both
            del self.nodeDict[glabel] #removing the g node from the node dict since no longer a nj node
            print("NJ part updated")


            #updating the GNJ matrix

            D0_GNJ= self.GNJpart.copy()
            # print(D0_GNJ)
            D0_GNJ = np.delete(D0_GNJ,imin,0) #removing g row as it is no longer a NJ node
            D0_GNJ = np.delete(D0_GNJ,jmin,1) #removing f column as it is no longer a placeholder node
            self.labelsGNJ.remove(self.labelsGNJ[jmin])
            fparentindex= self.labelsNJ.index(fparent)
            for i in self.nodeDict[fparent]: #so this step is becoming o(n^2) so ask if this is okay or if this could be optimized
                t= self.labelsGNJ.index(i[0]) #finding the index of the label of child in the labels list hence the current GNJ matrix
                # print(D0_GNJ)
                D0_GNJ[:,t]= D0[:,fparentindex]+i[1] #adding the distance of the newnode(or u) with the appropriate constant distance of its child and updating the column of child's label 
            print("GNJ part updated")
            self.DistMat=D0
            self.GNJpart=D0_GNJ
            self.distsums=self.distSum(self.DistMat)
            print("vector sum updated")
