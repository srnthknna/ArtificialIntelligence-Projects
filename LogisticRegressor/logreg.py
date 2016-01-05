'''
Created on Oct 30,2015

@author: srnthknna
'''
import csv
import math
import random
import sys
import matplotlib.pyplot as g1
import matplotlib.pyplot as g2
list=[]
errorlist=[]
weights=[]
#method to read the sample csv file
def readsamples():
	global list
	with open(sys.argv[1], newline='') as f:
		reader = csv.reader(f)
		for row in reader:
			elem=[]
			for x in row:
				elem.append(float(x))
			list.append(elem)
#method to write the weights vector in a csv 
def writeweights():
	global weights
	with open('weights.csv', 'w', newline='') as f:
		writer = csv.writer(f)
		writer.writerow(weights)
#method to read the weights.csv	
def readweights():
	global weights
	with open(sys.argv[2], newline='') as f:
		reader = csv.reader(f)
		for row in reader:
			for x in row:
				weights.append(float(x))

#method to calculate the sigmoid function
def hwx(x):
    f=1/(1+math.e**(-x))
    return f
    
#method to perform the linear regression   
def l():
    global list,errorlist,weights
	#weights are randomly assigned
    w0=random.uniform(-20,20)
    w1=random.uniform(-20,20)
    w2=random.uniform(-20,20)
    previous=0;
    current=0;
    for k in range(100):
        previous=current
        current=0
        for i in range(len(list)):
            (x1,x2,Y)=list[i]       
            sum=0
            sum1=0
            sum2=0
			#alpha is randomly assigned
            aplha=random.uniform(0.001,0.1)
            for j in range(1+i):
                (a1,a2,a3)=list[j]
                exp=w0+(w1*a1)+(w2*a2)
				#to calculate the error loss of each epoch
                if(i==len(list)-1):
                    current=current+(a3-hwx(exp))**2
                sum=sum+(a3-hwx(exp))
                sum1=sum1+(a3-hwx(exp))*a1
                sum2=sum2+(a3-hwx(exp))*a2
            w0=w0+(aplha*sum)
            w1=w1+(aplha*sum1)
            w2=w2+(aplha*sum2)
			#to store the weights obtained
            weights=[w0,w1,w2]
        errorlist.append(current)
		#if the error loss is below 0.001 and if the current error rate is below 0.5 we terminate the loop
        if(abs(current-previous)<0.001 and current<0.5 ):
            break
        else:
            continue

#method to print the report for classified samples
def counter():
	global list,weights
	total0=0;
	total1=0;
	for elements in  list:
		(_,_,z)=elements
		if z==1:
			total1=total1+1
		else:
			total0=total0+1
	incorrect0=0;
	incorrect1=0;
	for elements in list:
		(x,y,z)=elements
		if(weights[0]+weights[1]*x+weights[2]*y<0 and z==1):
			incorrect0=incorrect0+1;
		elif(weights[0]+weights[1]*x+weights[2]*y>0 and z==0):
			incorrect1=incorrect1+1;
	print ("Number of elements in class 0: ",total0)
	print ("Number of incorrectly classified for class 0: ",incorrect0)
	print ("Number of elements in class 1: ",total1)
	print ("Number of incorrectly classified for class 1: ",incorrect1)

#method to print the graph for epoch vs error loss
def graph1():
	values=[]
	for i in range(len(errorlist)):
		values.append(i+1)
	g1.xlabel(' epoch count ')
	g1.ylabel(' sum of the squared error ')
	g1.scatter(values,errorlist,color='orange')
	g1.plot(values,errorlist)
	g1.show()

#method to print the graph for samples and the line separating them
def graph2():
	global list,weights
	pointsx=[]
	pointsy=[]
	points1x=[]
	points1y=[]
	for elements in list:
		(x,y,z)=elements
		if(z==1):
			pointsx.append(x)
			pointsy.append(y)
		else:
			points1x.append(x)
			points1y.append(y)
	
	g1.scatter(pointsx,pointsy,color='blue',label='class 0')
	g1.scatter(points1x,points1y,color='orange',label='class 1')
	g1.legend()
	minx=min(min(pointsx),min(pointsx))-5
	miny=-1*(weights[0]+weights[1]*minx)/weights[2]
	maxx=max(max(pointsx),max(pointsx))+5
	maxy=-1*(weights[0]+weights[1]*maxx)/weights[2]
	g1.plot([minx,maxx],[miny,maxy])	
	g1.show()

#main method begins here
def main():
	#if only sample csv file is provided
	if (len(sys.argv)==2):
		readsamples()
		l()
		writeweights()
		graph1()
	#if sample csv and weights csv is provided
	elif (len(sys.argv)==3):
		readweights()
		readsamples()
		counter()
		graph2()
	else :
		print("Wrong number of arguments")
main()