'''
Created on Nov 15, 2015

@author: srnthknna
'''
import csv
import math
import random
from _random import Random
import copy
import sys
import matplotlib.pyplot as g1
import matplotlib.pyplot as g2
import matplotlib.pyplot as g3
import matplotlib.pyplot as g4
import matplotlib.pyplot as g5
list=[]
list0=[]
values01=[]
values0=[]
classifier0=[]
xyvals0=[]
values01_0=[]
weights0=[]

numinputs=3
numhidden=6
numoutput=4 

rates=[[20,-7,-7,-7],[-7,15,-7,-7],[-7,-7,5,-7],[-3,-3,-3,-3]]
cmatrix0=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]

#method to find sigmoid
def hwx(x):
    f=1/(1+math.e**(-x))
    return f
#method to read the samples from file
def readsamples(filename):
    global list,list0
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            elem=[]
            for x in row:
                elem.append(float(x))
            list.append(elem)
    list0=copy.deepcopy(list)

#class to represent perceptron	
class node():
    w=[]
    v=0
    d=0
    b=0
#class for neural network
class network():
    input=[]
    hidden=[]
    output=[]
    layers=[]       
    def __init__(self):
        self.input=[]
        self.hidden=[]
        self.output=[]
        self.layers=[] 
        for i in range(numinputs):
            n=node()
            l=[]
            for w in range(numhidden):
                l.append(random.uniform(1,1))
            n.w=l
            self.input.append(n)
        self.input[numinputs-1].v=1
        self.input[numinputs-1].b=1        
        for i in range(numhidden):
            n=node()
            l=[]
            for w in range(numoutput):
                l.append(random.uniform(1,1))
            n.w=l
            self.hidden.append(n)
        self.hidden[numhidden-1].v=1
        self.hidden[numhidden-1].b=1        
        for i in range(numoutput):
            n=node()
            self.output.append(n)   
        self.layers.append(self.input)
        self.layers.append(self.hidden)
        self.layers.append(self.output) 
a0=network()
#method to read the weights file 
def weightsread(filename):
    global weights0,weights10,weights100,weights1000,weights10000
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            elem=[]
            for x in row:
                elem.append(float(x))
            weights0.append(elem)

#method to assign the class to test data
def assignnets():
    global weights0
    count=0
    for l in range(len(a0.layers)-1):
        for i in a0.layers[l]: 
            i.w=weights0[count]
            count=count+1
    
#method to classify the data
def forproc(a,values,list):    
    for example in list: 
        v=[]
        for i in range(numinputs-1):
            a.layers[0][i].v=example[i]
            
        for h in range(1,len(a.layers)):    
            for j in range(len(a.layers[h])):
                sum=0
                for i in a.layers[h-1]:
                    sum=sum+(i.w[j]*i.v) 
                sum=hwx(sum) 
                if(a.layers[h][j].b==0):    
                    a.layers[h][j].v=sum
                if(h==(len(a.layers)-1)):
                    v.append(a.layers[h][j].v)
        values.append(v)
		
#method to assign the class values
def assignclassifier(values,classifier,classifiedlist):
    for i in values:
        a=max(i)
        b=i.index(a)+1
        classifier.append(b)
    for i in range(len(classifier)):
        classifiedlist[i][2]=classifier[i]

#method to find the recognition rate    
def recograte(classifier):
    global list
    correct=0
    for i in range(len(list)):
        if(list[i][2]==classifier[i]):
            correct=correct+1
    print("Total samples ",len(list))
    print("Percentage of correct classification ",(correct/len(list)*100))    
#method to print profit
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

#method to create the data for plotting regions
def datacreate():
	global xyvals0,xyvals10,xyvals100,xyvals1000,xyvals10000
	xyvals=[]
	for i in range(0,100,1):
		for j in range(0,100,1):
			list=[]
			list.append(i/100)
			list.append(j/100)
			list.append(1)
			xyvals.append(list)
	xyvals0=copy.deepcopy(xyvals)
#method to assign class values	
def assignclassclassifier(values,list):
    temp=[]
    for i in values:
        a=max(i)
        b=i.index(a)+1
        temp.append(b)
    for i in range(len(temp)):
        list[i][2]=temp[i]
#method to print the plot for regions and test data
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
	g1.title('Region for the each class ')
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
		weightsfile=sys.argv[1]
		datafile=sys.argv[2]
		weightsread(weightsfile)
		assignnets()            
		readsamples(datafile)

		forproc(a0,values0,list)	
		assignclassifier(values0,classifier0,list0)
		recograte(classifier0)
		profitcalc(classifier0,cmatrix0)
		confusionmat(cmatrix0)
	
		datacreate()
		forproc(a0,values01_0,xyvals0)
		assignclassclassifier(values01_0,xyvals0)
		graph2(xyvals0,g1,1)
		g1.show()
main()