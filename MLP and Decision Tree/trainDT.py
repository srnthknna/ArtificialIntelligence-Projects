import csv
import math
import random
import copy
import sys
from _random import Random
from _operator import itemgetter
import matplotlib.pyplot as g1
import matplotlib.patches as patches
import pickle

list=[]
test=[]
#method to write the tree in a file
def writetree(root,name):
    pickle.dump( root, open( name, "wb" ) )
#method to read a tree from a file
def readsamples(filename):
    global list
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            elem=[]
            for x in row:
                elem.append(float(x))
            list.append(elem)
#method to read test data
def treadsamples():
    global test
    with open('sd.csv', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            elem=[]
            for x in row:
                elem.append(float(x))
            test.append(elem)

#method to traverse the tree
def bst(root,record):
    if(root != None ):
        
        if(record[root.attributeindex]<root.threshold):
            if(root.left!=None):
                return bst(root.left,record)
            else:
                return findnonzero(root.classval)
        else:
            if(root.right!=None):
                return bst(root.right,record)
            else:
                return findnonzero(root.classval)

#method to find the first zero       
def findnonzero(list):
    for i in range(len(list)):
        if list[i]!=0:
            return i+1
    return 0
    
#method to count the nodes
def countnodes(root):
    if(root==None):
        return 0
    else:
        return (1+countnodes(root.left)+countnodes(root.right))
#method to count the leaf    
def countleaf(root):
    if(root.left==None and root.right==None):

        return 1
    else:
        return (countleaf(root.left)+countleaf(root.right)) 
leafdepths=[]
#method to assign the leaf depths
def assignleafd(root):     
    if(root.left==None and root.right==None):
        leafdepths.append(root.d)
    else:
        assignleafd(root.left)
        assignleafd(root.right)   

drawlist=[]
#method to do breadth first search
def bfs(root):
    global drawlist
    queue=[]
    queue.append(root)
    while(len(queue)>0):
        current=queue.pop(0)
        if(current.left!=None and current.right!=None):
            third=0
            if(current.parent!=None and current.parent.left==current):
                third=1
            elif(current.parent!=None and current.parent.right==current):
                third=2
            drawlist.append([current.threshold,current.attributeindex,third])
        if(current.left!=None):
            queue.append(current.left)
        if(current.right!=None):
            queue.append(current.right)  
          
#method to print the summary        
def printsummary(root):
    global leafdepths
    (numberofnodes,numberofleafs)=(countnodes(root),countleaf(root))
    assignleafd(root)
    (maxt,mint,averaget)=(max(leafdepths),min(leafdepths),(sum(leafdepths)/len(leafdepths)))  
    print()
    print ("Summary of Tree ")
    print ("Number of Nodes ",numberofnodes)
    print ("Number of Leafs",numberofleafs)
    print ("Maximum depth of leaf from root ",maxt)
    print ("Minimum depth of leaf from root ",mint)
    print ("Average depth of leaf from root ",averaget)    
#class to represent perceptron
class node():
    def __init__(self):
        self.threshold=0
        self.attributeindex=0
        self.parent=None
        self.left=None
        self.right=None
        self.classval=[0,0,0,0]
        self.data=[]
        self.d=0
    def displaynode(self):
        print(self.threshold)
        print(self.attributeindex)
        print(self.parent)
        print(self.left)
        print(self.right)
        print(self.classval)
        print(self.data)
        print(self.d)

root=node()
#method to split the data with an attribute
def splitattribute():
    queue=[]
    root.data=list
    queue.append(root)
    count=0
    while (len(queue)>0):
        
        current=queue.pop(0)

        data=current.data
        leftsplit=[]
        rightsplit=[]       
        data1=sorted(data,key=itemgetter(0))
        data2=sorted(data,key=itemgetter(1))
  
        records=[]
        records.append(data1)
        records.append(data2)
        (bestt,besti,bestabove,bestbelow)=bestsplit(records)

        for i in range(len(data)):
            if(data[i][besti]<=bestt):
                leftsplit.append(data[i])
            else:
                rightsplit.append(data[i])

        count=count+1
        current.threshold=bestt
        current.attributeindex=besti
        if (len(leftsplit)>0 and bestbelow.count(0)<3 ):
            l=node()
            l.data=leftsplit
            l.parent=current
            l.classval=bestbelow
            l.d=current.d+1

            current.left=l
            queue.append(l)


        else:
            l=node()
            l.data=leftsplit
            l.parent=current
            l.classval=bestbelow
            current.left=l
            l.d=current.d+1


        if (len(rightsplit)>0 and bestabove.count(0)<3 ):
            r=node()
            r.data=rightsplit
            r.parent=current
            r.classval=bestabove
            r.d=current.d+1

            current.right=r
            queue.append(r)


        else:
            r=node()
            r.data=rightsplit
            r.parent=current
            r.classval=bestabove
            r.d=current.d+1

            current.right=r

    
#method to find the best split for all the data
def bestsplit(records):
    bestentropy=10
    bestt=0
    besti=0
    bestabove=[]
    bestbelow=[]

    for i in range(len(records)):
        for j in range(len(records[i])-1):
            thresh=(records[i][j][i]+records[i][j+1][i])/2            
            classabove=[0,0,0,0]
            classbelow=[0,0,0,0]
            for k in range(len(records[i])):
                val=records[i][k][i]
                classval=records[i][k][2]
                if(val<thresh):
                    classbelow[int(classval)-1]=classbelow[int(classval)-1]+1
                else:
                    classabove[int(classval)-1]=classabove[int(classval)-1]+1
            entropy1=0
            for num in range(len(classbelow)):
                if(classbelow[num]!=0):
                    entropy1=entropy1-1*classbelow[num]/sum(classbelow)*(math.log2(classbelow[num]/sum(classbelow)))
                else:
                    entropy1=entropy1-1*classbelow[num]/sum(classbelow)*(math.log2(1/sum(classbelow)))

            entropy2=0
            for num in range(len(classabove)):
                if(classabove[num]!=0):
                    entropy2=entropy2-1*classabove[num]/sum(classabove)*(math.log2(classabove[num]/sum(classabove)))
                else:
                    entropy2=entropy2-1*classabove[num]/sum(classabove)*(math.log2(1/sum(classabove)))

            entropy=entropy1*(sum(classbelow)/(sum(classabove)+sum(classbelow)))+entropy2*(sum(classabove)/(sum(classabove)+sum(classbelow)))

            if(entropy<bestentropy):
                bestentropy=entropy
                bestt=thresh
                besti=i
                bestabove=classabove
                bestbelow=classbelow


    return (bestt,besti,bestabove,bestbelow)

rectcoordinates=[0,1,1,1]  
#method to find boundaries
def func():
    g1.plot([0,1],[1,1])
    g1.plot([1,0],[1,1])
    g1.plot([0,0],[0,1])
    g1.plot([0,0],[1,0])
#method to print boundaries of attributes
def graph1(root,coord,i):
    g1.figure(i)
    titles=["Decision Tree","Chi Square Pruned Tree"]
    
    if(root.parent==None):
        g1.plot([0,1],[1,1])
        g1.plot([0,1],[0,0])
        g1.plot([1,1],[1,0])
        g1.plot([0,0],[1,0])
        points()
        g1.title(titles[i-1])
    
    if(root.left!=None and root.right!=None and root.attributeindex==0):

        newcoord=[coord[0],coord[1],root.threshold,coord[3]]
        g1.plot([newcoord[0]+newcoord[2],newcoord[0]+newcoord[2]],[1-newcoord[1],1-abs(newcoord[1]-newcoord[3])])
        if root.left!=None:
            graph1(root.left,newcoord,i)
        newcoord1=[newcoord[2],newcoord[1],abs(coord[2]-newcoord[2]),newcoord[3]]
        if root.right!=None:
            graph1(root.right,newcoord1,i)
    if(root.left!=None and root.right!=None and root.attributeindex==1):

        newcoord=[coord[0],coord[1],coord[2],root.threshold]
        g1.plot([newcoord[0],newcoord[0]+newcoord[2]],[1-abs(newcoord[1]-newcoord[3]),1-abs(newcoord[1]-newcoord[3])])
        if root.left!=None:
            graph1(root.left,newcoord,i)
        newcoord1=[newcoord[0],root.threshold,newcoord[2],abs(coord[3]-newcoord[3])]
        if root.right!=None:
            graph1(root.right,newcoord1,i)
    return
#method to print the Train data    
def points():
    ppoints1x=[]
    ppoints1y=[]
    ppoints2x=[]
    ppoints2y=[]
    ppoints3x=[]
    ppoints3y=[]
    ppoints4x=[]
    ppoints4y=[]
    for elements in list:
        (x,y,z)=elements
        if(z==1):
            ppoints1x.append(x)
            ppoints1y.append(y)
        elif(z==2):
            ppoints2x.append(x)
            ppoints2y.append(y)
        elif(z==3):
            ppoints3x.append(x)
            ppoints3y.append(y)
        else:
            ppoints4x.append(x)
            ppoints4y.append(y)    
    g1.scatter(ppoints1x,ppoints1y,color='blue',label='-Bolts')
    g1.scatter(ppoints2x,ppoints2y,color='black',label='-Nuts')
    g1.scatter(ppoints3x,ppoints3y,color='yellow',label='-Rings')
    g1.scatter(ppoints4x,ppoints4y,color='green',label='-Scrap')
    g1.legend()    
#method to traverse the chi square tree
def chisquaretraverse(root,penleaf):
    if(root.left!=None and root.right != None and root.left.left==None and root.left.right==None or root.right.left==None and root.right.right==None  ):
        penleaf.append(root)  
    elif(root.left!=None):
            chisquaretraverse(root.left,penleaf) 
    elif(root.right!=None):
            chisquaretraverse(root.right,penleaf)
    return penleaf

chialphatable=[0,3.841,5.991,7.815,9.488]
#chi1percent=[0,6.635,9.210,11.345,13.277]
#method to prune the tree
def prune(root):
    currentnodes=countnodes(root)
    previousnodes=0
    while(currentnodes!=previousnodes):

        penleaf=[]
        penleaf=chisquaretraverse(root,penleaf)
        #print(penleaf)
 
        for i in penleaf:
            expectedl=[] 
            for c in i.classval:
                expectedl.append(c/sum(i.classval)*sum(i.left.classval))
            expectedr=[]
            for c in i.classval:
                expectedr.append(c/sum(i.classval)*sum(i.right.classval))
            leftsum=0
            rightsum=0
            for k in range(len(expectedl)):
                if(expectedl[k]!=0):
                    leftsum=leftsum+(i.left.classval[k]-expectedl[k])**2/expectedl[k]
                else:
                    leftsum=leftsum+(i.left.classval[k]-expectedl[k])**2/1
            for k in range(len(expectedr)):
                if(expectedr[k]!=0):
                    rightsum=rightsum+(i.right.classval[k]-expectedr[k])**2/expectedr[k]
                else:
                    rightsum=rightsum+(i.right.classval[k]-expectedr[k])**2/1
            delta=leftsum+rightsum
            degree=3-i.classval.count(0)
            if (chialphatable[degree]>delta):
                i.left=None
                i.right=None
        previousnodes=currentnodes
        currentnodes=countnodes(root)

def main():
    if len(sys.argv) != 2:
        print("Invalid Arguments")
        return
    else:
        filename=sys.argv[1]    
        readsamples(filename)       
        splitattribute()
        writetree(root,"Decision.p")
        print("Decision Tree")
        printsummary(root)
        print()
        print()
        graph1(root,rectcoordinates,1)
        print("Chi Square Pruning")
        rootchi=copy.deepcopy(root)
        prune(rootchi)
        writetree(rootchi,"ChiSquare.p")
        printsummary(rootchi)
        graph1(rootchi,rectcoordinates,2)
        g1.show()
main()