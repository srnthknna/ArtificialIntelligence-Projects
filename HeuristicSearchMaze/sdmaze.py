import sys
import copy

nodesvisited = 1
nodescount = 1

#heuristic functions 
def heuristic2(i, j, sdmaze):
    (a, b) = findG(sdmaze)
    c = max(abs(a - i), abs(b - j))
    d = min(abs(a - i), abs(b - j))
    distance = 3*d 
    return distance

def heuristic1(i, j, sdmaze):
    (a, b) = findG(sdmaze)
    c = max(abs(a - i), abs(b - j))
    d = min(abs(a - i), abs(b - j))
    distance = (d * c) / 2
    return distance

def heuristic3(i, j, sdmaze):
    (a, b) = findG(sdmaze)
    c = max(abs(a - i), abs(b - j))
    d = min(abs(a - i), abs(b - j))
    distance = (d*d)*(2**0.5)+abs(c-d)
    return distance

#method to read the maze from the file
def readsdmaze(filename):
    maze=[]
    file = open ( filename , 'r')
    for line in file:
        row=[]
        for i in range(len(line)):
            row.append(line[i])
        maze.append(row)
    return maze

#Node class with die and position
class Node:
    #constructor
    def __init__(self, i, j):
        self.die = {"top":1, "front":5, "right":3}
        self.j = j
        self.previous = None
        self.sucessors = []
        self.heuristicCost = 0
        self.nodeCost = 0
        self.moveTaken = None
        self.i = i
    #method to generate a node with die moving down in the maze
    def adddown(self, i, j, sdmaze, dielist, heuristic):
        if(isObstacle(sdmaze, i + 1, j) and "down" in dielist.keys()):
            a = Node(i + 1, j)
            a.previous = self
            a.heuristicCost = self.nodeCost + heuristic(a.i, a.j, sdmaze)
            a.nodeCost = self.nodeCost + 1
            a.die = dielist["down"]
            a.moveTaken = "down"
            self.sucessors.append(a)
    #method to generate a node with die moving right in the maze
    def addright(self, i, j, sdmaze, dielist, heuristic):
        if(isObstacle(sdmaze, i, j + 1) and "right" in dielist.keys()):
            a = Node(i, j + 1)
            a.previous = self
            a.nodeCost = self.nodeCost + 1
            a.heuristicCost = self.nodeCost + heuristic(a.i, a.j, sdmaze)
            a.die = dielist["right"]
            a.moveTaken = "right"
            self.sucessors.append(a)
    #method to generate a node with die moving left in the maze          
    def addleft(self, i, j, sdmaze, dielist, heuristic):
        if(isObstacle(sdmaze, i, j - 1) and "left" in dielist.keys()):
            a = Node(i, j - 1)
            a.previous = self
            a.nodeCost = self.nodeCost + 1
            a.heuristicCost = self.nodeCost + heuristic(a.i, a.j, sdmaze)
            a.die = dielist["left"]
            a.moveTaken = "left"
            self.sucessors.append(a)   
    #method to generate a node with die moving up in the maze
    def addup(self, i, j, sdmaze, dielist, heuristic):
        if(isObstacle(sdmaze, i - 1, j) and "up" in dielist.keys()):
            a = Node(i - 1, j)
            a.previous = self
            a.nodeCost = self.nodeCost + 1
            a.heuristicCost = self.nodeCost + heuristic(a.i, a.j, sdmaze)
            a.die = dielist["up"]
            a.moveTaken = "up"
            self.sucessors.append(a) 
    #method to check if the goal state is reached
    def isGoal(self, sdmaze):
        if(sdmaze[self.i][self.j] == 'G' and self.die["top"] == 1):
            return True
        return False
    #methods to compare node objects
    def __eq__(self, other):
        return (self.heuristicCost == other.heuristicCost)
    def __le__(self, other):
        return (self.heuristicCost <= other.heuristicCost)
    def __lt__(self, other):
        return (self.heuristicCost < other.heuristicCost)  
    def __ge__(self, other):
        return (self.heuristicCost >= other.heuristicCost)
    def __gt__(self, other):
        return (self.heuristicCost > other.heuristicCost)  
    def __ne__(self, other):
        return (self.heuristicCost != other.heuristicCost)
    def __cmp__(self, other):
        if self.heuristicCost > other.heuristicCost:
            return 1
        elif self.heuristicCost < other.heuristicCost:
            return -1
        else:
            return 0
#method to print the maze    
def printsdmaze(sdmaze):
    row = len(sdmaze)
    col = len(sdmaze[0])
    for i in range(row):
        for j in range(col-1):
            print(format(sdmaze[i][j]), end=" ")
        print()
#method to check if there is an obstacle in the maze
def isObstacle(sdmaze, i, j):
    if(sdmaze[i][j] != '*'):
        return True
    return False 
#method to generate all possible die movements from the current die configuration
def dieSuccessor(die):
    a, b, c, d = {"top":0, "right":0, "front":0}, {"top":0, "right":0, "front":0}, {"top":0, "right":0, "front":0}, {"top":0, "right":0, "front":0}   
    list = {}
    #left movement die
    a["top"] = die["right"]
    a["right"] = 7 - die["top"]
    a["front"] = die["front"]
    #right movement die
    b["top"] = 7 - die["right"]
    b["right"] = die["top"]
    b["front"] = die["front"]
    #up movement die
    c["top"] = die["front"]
    c["right"] = die["right"]
    c["front"] = 7 - die["top"]
    #down moviement die
    d["top"] = 7 - die["front"]
    d["right"] = die["right"]
    d["front"] = die["top"]
    if(a["top"] != 6):
        list["left"] = a
    if(b["top"] != 6):
        list["right"] = b
    if(c["top"] != 6):
        list["up"] = c
    if(d["top"] != 6):
        list["down"] = d       
    return list
#method to find start state in maze
def findS(sdmaze):
    row = len(sdmaze)
    col = len(sdmaze[0])
    for i in range(row):
        for j in range(col):
            if(sdmaze[i][j] == 'S'):
                return(i, j)
    return (-1, -1)
#method to find goal state in maze
def findG(sdmaze):
    row = len(sdmaze)
    col = len(sdmaze[0])
    for i in range(row):
        for j in range(col):
            if(sdmaze[i][j] == 'G'):
                return(i, j)
    return (-1, -1)
#method to find successors of the nodes
def sucessors(node, sdmaze, heuristic):
    row = len(sdmaze)
    col = len(sdmaze[0])
    dielist = dieSuccessor(node.die)
    i = node.i
    j = node.j
    #check all the boundary cells
    if(i == 0 and j == 0):
        node.adddown(i, j, sdmaze, dielist, heuristic)
        node.addright(i, j, sdmaze, dielist, heuristic)
    elif(i == 0 and j == col - 1):
        node.adddown(i, j, sdmaze, dielist, heuristic)
        node.addleft(i, j, sdmaze, dielist, heuristic)
    elif(i == row - 1 and j == 0):
        node.addup(i, j, sdmaze, dielist, heuristic)
        node.addright(i, j, sdmaze, dielist, heuristic)
    elif(i == row - 1 and j == col - 1):
        node.addup(i, j, sdmaze, dielist, heuristic)
        node.addleft(i, j, sdmaze, dielist, heuristic)
    #check all the edges
    elif(i == 0):
        node.adddown(i, j, sdmaze, dielist, heuristic)
        node.addright(i, j, sdmaze, dielist, heuristic)
        node.addleft(i, j, sdmaze, dielist, heuristic)
    elif(i == row - 1):
        node.addup(i, j, sdmaze, dielist, heuristic)
        node.addright(i, j, sdmaze, dielist, heuristic)
        node.addleft(i, j, sdmaze, dielist, heuristic)
    elif(j == 0):
        node.addup(i, j, sdmaze, dielist, heuristic)
        node.adddown(i, j, sdmaze, dielist, heuristic)
        node.addright(i, j, sdmaze, dielist, heuristic)
    elif(j == col - 1):
        node.addup(i, j, sdmaze, dielist, heuristic)
        node.adddown(i, j, sdmaze, dielist, heuristic)
        node.addleft(i, j, sdmaze, dielist, heuristic)
    #if the cell is in the middle
    else:
        node.addup(i, j, sdmaze, dielist, heuristic)
        node.adddown(i, j, sdmaze, dielist, heuristic)
        node.addright(i, j, sdmaze, dielist, heuristic)
        node.addleft(i, j, sdmaze, dielist, heuristic)
    return node.sucessors
#method for a* algorithm
def astar(sdmaze, h):
    global nodesvisited
    global nodescount
    (si, sj) = findS(sdmaze)
    (gi, gj) = findG(sdmaze)
    #start node
    node = Node(si, sj)
    node.heuristicCost = h(si, sj, sdmaze)
    root = str(node.i) + str(node.j) + str(node.die["top"]) + str(node.die["front"]) + str(node.die["right"])
    #add  start state to dictionary and priority queue
    visited = {}
    visited[root] = node
    node.sucessors = sucessors(node, sdmaze, h)
    pqueue = []
    pqueue.append(node)
    nodesvisited = nodesvisited + 1
    #while priority queue is not empty
    while(len(pqueue) > 0 ):
        pqueue.sort()
        top=pqueue.pop(0)
        nodesvisited = nodesvisited + 1
        #if state is goal then return node
        if(top.isGoal(sdmaze)):
            return top        
        #else add successors to priority queue
        for child in top.sucessors:           
            nodescount = nodescount + 1
            children = str(child.i) + str(child.j) + str(child.die["top"]) + str(child.die["front"]) + str(child.die["right"])
            if(children not in visited.keys()):
                visited[children] = child
                child.sucessors = sucessors(child, sdmaze, h)
                pqueue.append(child)         
 #main method starts here       
def main():
    global nodescount
    global nodesvisited
    
    if(len(sys.argv) != 2):
        print("Give a sdmaze file name")
        sys.exit()
    sdmazefile = sys.argv[1]

    
    #Three mazes for three heuristics
    sdmaze1 = readsdmaze(sdmazefile)
    sdmaze2 = copy.deepcopy(sdmaze1)
    sdmaze3 = copy.deepcopy(sdmaze1)

    print("solution for heuristic 1")
    answer = astar(sdmaze1, heuristic1)
    steps = []
    print("nodesvisited")
    print(nodesvisited)
    print("nodescount")
    print(nodescount)
    print("step count")
    if(answer is not None):
        while(answer.previous is not None):
            steps.insert(0, answer)
            answer = answer.previous
        steps.insert(0, answer)   
        print(len(steps) - 1)
        for i in steps:
            print("Current die configuration is ", i.die)
            print("Move Taken", i.moveTaken)
            sdmaze1[i.i][i.j] = 'D'
            printsdmaze(sdmaze1)
        print()
        print()
    else:
        print("No solution")
        print()
        print()
    nodescount = 0
    nodesvisited = 0
    print("solution for heuristic 2")
    answer = astar(sdmaze2, heuristic2)
    steps = []
    print("nodesvisited")
    print(nodesvisited)
    print("nodescount")
    print(nodescount)
    print("step count")
    if(answer is not None):
        while(answer.previous is not None):
            steps.insert(0, answer)
            answer = answer.previous
        steps.insert(0, answer) 
        print(len(steps) - 1)
        for i in steps:
            print("Current die configuration is ", i.die)
            print("Move Taken", i.moveTaken)
            sdmaze2[i.i][i.j] = 'D'
            printsdmaze(sdmaze2)
        print()
        print()
    else:
        print("No solution")
        print()
        print()
    nodescount = 0
    nodesvisited = 0
    print("solution for heuristic 3")
    answer = astar(sdmaze3, heuristic3)
    steps = []
    print("nodesvisited")
    print(nodesvisited)
    print("nodescount")
    print(nodescount)
    print("step count")
    if(answer is not None):
        while(answer.previous is not None):
            steps.insert(0, answer)
            answer = answer.previous
        steps.insert(0, answer) 
        print(len(steps) - 1)
        for i in steps:
            print("Current die configuration is ", i.die)
            print("Move Taken", i.moveTaken)
            sdmaze3[i.i][i.j] = 'D'
            printsdmaze(sdmaze3)
        print()
        print()
    else:
        print("No solution")
        print()
        print()


main()
