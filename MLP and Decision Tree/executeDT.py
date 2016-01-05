import csv
import math
import random
import copy
import sys
from _random import Random
from _operator import itemgetter
import matplotlib.pyplot as g1
import pickle

list=[]
rates=[[20,-7,-7,-7],[-7,15,-7,-7],[-7,-7,5,-7],[-3,-3,-3,-3]]
cmatrix=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
classifier1=[]
classifierxy=[]
xyvals=[]

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

#method to do the binary search traversal
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

#method to read the samples
def readsamples(datafile):
    global list
    with open(datafile, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            elem=[]
            for x in row:
                elem.append(float(x))
            list.append(elem)    
#method to find the first non zeror        
def findnonzero(list):
    for i in range(len(list)):
        if list[i]!=0:
            return i+1
    return 0
    
#method to assign the class values            
def setclassdetails(classifier,root,list):
    for i in list:
        cval=bst(root,i)
        classifier.append(cval)

#method to print the recognition rate    
def recograte(classifier):
    global list
    correct=0
    for i in range(len(list)):
        if(list[i][2]==classifier[i]):
            correct=correct+1
    print("Total samples ",len(list))
    print("Percentage of correct classification ",(correct/len(list)*100))    
#method to print the profit
def profitcalc(classifier,cmatrix):
    global list  
    profit=0
    for k in range(len(list)):
        j=int(list[k][2]-1)
        i=int(classifier[k]-1)
        cmatrix[i][j]=cmatrix[i][j]+1

        profit=profit+rates[i][j]
    print("The profit obtained is ",profit)
#method to print the confusion matrix
def confusionmat(cmatrix):
    print("         Confusion Matrix")
    print("Assigned               Actual              ")
    print("            Bolt    Nut    Ring    Scrap ")
    print("Bolt        {0}        {1}       {2}       {3}   ".format(cmatrix[0][0],cmatrix[0][1],cmatrix[0][2],cmatrix[0][3]))
    print("Nut         {0}        {1}       {2}       {3}   ".format(cmatrix[1][0],cmatrix[1][1],cmatrix[1][2],cmatrix[1][3]))
    print("Ring        {0}        {1}       {2}       {3}   ".format(cmatrix[2][0],cmatrix[2][1],cmatrix[2][2],cmatrix[2][3]))
    print("Scrap       {0}        {1}       {2}       {3}   ".format(cmatrix[3][0],cmatrix[3][1],cmatrix[3][2],cmatrix[3][3]))

#method to read the object from file    
def read(name):
    return pickle.load( open( name, "rb" ) )
#method to create the data for the region
def datacreate():
    global xyvals
    xyvals=[]
    for i in range(0,100,1):
        for j in range(0,100,1):
            list=[]
            list.append(i/100)
            list.append(j/100)
            list.append(1)
            xyvals.append(list)
    xyvals=copy.deepcopy(xyvals)
#method to assign the class values
def assignclassclassifier(values,list):
    temp=[]
    for i in values:
        a=max(i)
        b=i.index(a)+1
        temp.append(b)
    for i in range(len(temp)):
        list[i][2]=temp[i]    
#method to assign the class details
def assignclassdetails(classifier,xyval):
    for i in range(len(xyval)):
        xyval[i][2]=classifier[i]
#method to print the graph for decision tree boundaries
def graph2(region,g1,i):
    points1x=[]
    points1y=[]
    points2x=[]
    points2y=[]
    points3x=[]
    points3y=[]
    points4x=[]
    points4y=[]
    ppoints1x=[]
    ppoints1y=[]
    ppoints2x=[]
    ppoints2y=[]
    ppoints3x=[]
    ppoints3y=[]
    ppoints4x=[]
    ppoints4y=[]
    for elements in region:
        (x,y,z)=elements
        if(z==1):
            points1x.append(x)
            points1y.append(y)
        elif(z==2):
            points2x.append(x)
            points2y.append(y)
        elif(z==3):
            points3x.append(x)
            points3y.append(y)
        else:
            points4x.append(x)
            points4y.append(y)
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
    g1.figure(i)
    g1.scatter(points1x,points1y,color='blue',label='Bolts')
    g1.scatter(points2x,points2y,color='orange',label='Nuts')
    g1.scatter(points3x,points3y,color='red',label='Rings')
    g1.scatter(points4x,points4y,color='cyan',label='Scrap')
    g1.scatter(ppoints1x,ppoints1y,color='white',label='-Bolts')
    g1.scatter(ppoints2x,ppoints2y,color='black',label='-Nuts')
    g1.scatter(ppoints3x,ppoints3y,color='yellow',label='-Rings')
    g1.scatter(ppoints4x,ppoints4y,color='green',label='-Scrap')
    g1.legend()

def main():
    if len(sys.argv) != 3:
        print("Invalid Arguments")
        return
    else:
        filename=sys.argv[1]
        datafile=sys.argv[2]         
        root=read(filename)
        readsamples(datafile)
        setclassdetails(classifier1,root,list)
        recograte(classifier1)
        profitcalc(classifier1,cmatrix)
        confusionmat(cmatrix)
        datacreate()
        setclassdetails(classifierxy,root,xyvals)
        assignclassdetails(classifierxy,xyvals)
        graph2(xyvals,g1,1)
        g1.show()
main()