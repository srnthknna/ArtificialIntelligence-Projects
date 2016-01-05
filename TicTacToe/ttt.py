'''
Created on Sep 19, 2015

@author: srnthknna
'''
import copy
#variables to count the states visited
minimaxCount=0
alphaBetaCount=0
#######################################
# Class Board 
#######################################
class Board():
    # constructor 
    def __init__(self):
        #data members game board, v value, move used to generate the v, successors for the node
        self.gameBoard=['-','-','-','-','-','-','-','-','-']
        self.v=-10
        self.move=-1
        self.successor=[]
    # places symbol in the board
    def placeSymbol(self,symbol,position):
        self.gameBoard[position]=symbol
    # places X in the board        
    def placeX(self,position):
        self.gameBoard[position]='X'
    # places O in the board    
    def placeO(self,position):
        self.gameBoard[position]='O'  
    # generates successors of the current node
    def successors(self,symbol):
        successor=[]
        for i in self.movesLeft():
            #creates a new board with deepcopy
            a=Board()
            a=copy.deepcopy(self);
            #mark the action which is taken in the successor
            a.move=i
            #symbol is placed in the action position
            a.placeSymbol(symbol,i)
            #add it to the successors list
            successor.append(a)
            #store it to the successors data member
        self.successor=(successor)
        return successor
    # checks if X has won the game
    def hasXWon(self):
        #horizontal rows check
        for i in [0,3,6]:
            if(self.gameBoard[i]==self.gameBoard[i+1]==self.gameBoard[i+2]=='X'):
                return True
        #vertical columns check    
        for i in [0,1,2]:
            if(self.gameBoard[i]==self.gameBoard[i+3]==self.gameBoard[i+6]=='X'):
                return True
        #diagonals check    
        if(self.gameBoard[0]==self.gameBoard[4]==self.gameBoard[8]=='X'or self.gameBoard[2]==self.gameBoard[4]==self.gameBoard[6]=='X'):
            return True
        return False
    # checks if O has won the game        
    def hasOWon(self):
        #horizontal rows check
        for i in [0,3,6]:
            if(self.gameBoard[i]==self.gameBoard[i+1]==self.gameBoard[i+2]=='O'):
                return True
        #vertical columns check
        for i in [0,1,2]:
            if(self.gameBoard[i]==self.gameBoard[i+3]==self.gameBoard[i+6]=='O'):
                return True
        #diagonals check    
        if(self.gameBoard[0]==self.gameBoard[4]==self.gameBoard[8]=='O'or self.gameBoard[2]==self.gameBoard[4]==self.gameBoard[6]=='O'):
            return True
        return False
    # checks is the game is drawn        
    def isDrawn(self):   
        for i in range(9):
            if(self.gameBoard[i]=='-'):
                return False
        return True
    # checks if the game 
    def isGameOver(self):
        if ( self.hasXWon() or self.hasOWon() ):
            return True
        elif (self.isDrawn()):
            return True
        else:
            return False
    # utility function which checks the winning possibilities of O's Game
    def utility(self):
        if(self.isGameOver() is True):
            if(self.hasXWon() is True):
                return -1
            elif(self.hasOWon() is True):
                return 1
            else:
                return 0 
    #display board function to print the board             
    def displayBoard(self):       
        #print('____________________')
        print('  {}  |   {}  |  {}  '.format(self.gameBoard[0],self.gameBoard[1],self.gameBoard[2]))
        print('____________________')
        print('  {}  |   {}  |  {}  '.format(self.gameBoard[3],self.gameBoard[4],self.gameBoard[5]))
        print('____________________')
        print('  {}  |   {}  |  {}  '.format(self.gameBoard[6],self.gameBoard[7],self.gameBoard[8]))     
        print('---------------------------------------------------------------------------------------------------------------')     
    #function left returns the functions left for the current node    
    def movesLeft(self):
        moves=[]
        #positions with '-' are taken as moves left
        for i in range(9):
            if(self.gameBoard[i]=='-'):
                moves.append(i)
        return moves
    #function for symbol change between the player turns
    def symbolChange(self,symbol):
        #if it is X it changes to O else X
        if (symbol=='X'):
            return 'O'
        else:
            return 'X'        
#####################################################        
#####minimax algorithm###############################    
#####################################################
    def minimax(self):
        #global variable to count the states
        global minimaxCount
        minimaxCount=0
        #call the max function with O's turn
        v=self.maxValue('O')
        #for all the successors from the current state
        for i in self.successor:
            #if the v value is present in the successors of the state then the corresponding action is returned
            if(i.v==v):
                a=i.move
                del self.successor
                return a
        return v
    #max function for minimax algorithm
    def maxValue(self,symbol):
        #global variable to count the states
        global minimaxCount
        #if game is over then utility value is returned
        if(self.isGameOver()):
            return self.utility()
        #dummy pre value representing -infinity
        v=-2
        #for all the successors maximum utility successors is searched
        for s in self.successors(symbol):
            minimaxCount=minimaxCount+1
            #maximum of the best move that the enemy takes is taken
            v=max(v,s.minValue(s.symbolChange(symbol)))
            #corresponding successors v value is stored
            s.v=copy.deepcopy(v)
            
        return v
    #min function for minimax algorithm
    def minValue(self,symbol):
        #global variable to count the states
        global minimaxCount
        #if game is over then utility value is returned
        if(self.isGameOver()):
            return self.utility()
        #dummy pre value representing infinity
        v=2
        #for all the successors minimum utility successors for the enemy is search
        for s in self.successors(symbol):
            minimaxCount=minimaxCount+1
            #minimum of the best move that the enemy takes is taken
            v=min(v,s.maxValue(s.symbolChange(symbol)))
            #corresponding successors v value is stored
            s.v=copy.deepcopy(v)
        return v
#####################################################        
#####alpha beta search algorithm#####################    
#####################################################
    def alphaBetaSearch(self):
        #global variable to count the states visited
        global alphaBetaCount
        alphaBetaCount=0
        #call the max funtion with O's turn with alpha -2 and 2 representing -infinity and infinity
        v=self.abmaxValue('O',-2,2)
        #for all the successors check if the action produces the corresponding v value
        for i in self.successor:
            if(i.v==v):
                a=i.move
                del self.successor
                return a
        return v
    #max function for alpha beta search algorithm
    def abmaxValue(self,symbol,a,b):
        #global variable to count states visited
        global alphaBetaCount
        #check if game is over and returns utility
        if(self.isGameOver()):
            return self.utility()
        #assigning v=-2 to represent -infinity
        v=-2
        #for all the successors from the current state
        for s in self.successors(symbol):
            alphaBetaCount+=1
            #calculate minimum of all the utility of states from enemy player
            v=max(v,s.abminValue(s.symbolChange(symbol),a,b))
            #stores the corresponding v value to the successors
            s.v=copy.deepcopy(v)
            #if v is greater than beta then break the loop
            if v>= b:
                return v
            #else replace alpha and continue with the loop
            a=max(a,v)
        return v
    #min function for alpha beta search algorithm
    def abminValue(self,symbol,a,b):
        #global variable to count states visited
        global alphaBetaCount
        #check if game is over and returns utility
        if(self.isGameOver()):
            return self.utility()
        #assigning v=2 to represent infinity
        v=2
        #for all the successors from the current state
        for s in self.successors(symbol):
            alphaBetaCount+=1
            #calculate the maximum of all the utility of states from enemy player
            v=min(v,s.abmaxValue(s.symbolChange(symbol),a,b))
            #stores the corresponding v value to the successors
            s.v=copy.deepcopy(v)
            #if v is less than alpha then break the loop and prune
            if v<=a:
                return v
            #else replace alpha and continue with the loop
            b=min(b,v)
        return v
################################################
#main function begins
#################################################
def main():
    #objects for alpha beta pruning and minimax algorithm boards
    ttt=Board()
    ttt1=Board()
    ttt.displayBoard()
    print('Welcome to TIC TAC TOE')
    print('Enter 0-9 for entering in the board, the values are entered horizontally')
    while( ttt.isGameOver() is False):
        #checks if the place is taken
        taken=False
        #prompts the user to enter the move
        while(taken is False):
            print("First Player")
            print('Enter a move')
            xMove=int(input())
            if(xMove not in ttt.movesLeft()):
                continue
            else:
                break
        #places the symbol in the board in position entered by the user    
        ttt.placeX(xMove)
        ttt.displayBoard()
        ttt1.placeX(xMove)
        #if game is over notify the winners and for draw scenario
        if( ttt.isGameOver() is True):
            if( ttt.hasOWon() is True):
                print("O won the game")
                break
            if( ttt.hasXWon() is True):
                print("X won the game")
                break
            if( ttt.isDrawn() is True):
                print("Game is Drawn")
                break
            break
        #place the symbols in the board through alpha beta pruning and minimax algorithm
        oMove=ttt.alphaBetaSearch()
        oMove1=ttt1.minimax()
        #print eh board and the number of nodes visited
        print('Nodes visited forAlpha-Beta Search ')
        print(alphaBetaCount)
        print("Computer's Turn on Alpha-Beta Search")
        ttt.placeO(oMove)
        ttt.displayBoard()
        print('Nodes visited for MiniMax ')
        print(minimaxCount)
        print("Computer's Turn on Minimax Search")
        ttt1.placeO(oMove1)
        ttt1.displayBoard()        
        #if game is over notify the winners and for draw scenario
        if( ttt.isGameOver() is True):
            if( ttt.hasOWon() is True):
                print("O won the game")
                break
            if( ttt.hasXWon() is True):
                print("X won the game")
                break
            if( ttt.isDrawn() is True):
                print("Game is Drawn")
                break
            break

#Execute the main program    
main()