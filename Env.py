
import random as rand
from os import system
import time
import numpy as np
import math
def clear():
    system("cls")

class Board_2048:

    def __init__(self,board_size ):
        self.dim=board_size
        self.board_size=(board_size*3)-2
        self.board=np.array([[0 for i in range(self.board_size)] for j in range(self.board_size) ])
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.check_in_board(i,j)==False:
                    self.board[i][j]=1
        self.reset()

    def reset(self):    
        self.board=np.array([[0 for i in range(self.board_size)] for j in range(self.board_size) ])
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.check_in_board(i,j)==False:
                    self.board[i][j]=1
        counter=2
        i=rand.randint(0,self.board_size-1)
        j=rand.randint(0,self.board_size-1)
        val=rand.randint(1,2)
        while counter!=0:
            if(self.check_in_board(i,j)==True):
                self.board[i][j]=val*2
                counter-=1
                # print(i,j)
            i=rand.randint(0,self.board_size-1)
            j=rand.randint(0,self.board_size-1)
            val=rand.randint(1,2)
        self.score=0
        self.max_invalid=0
        return self.board

    def print_board(self):
        for i in self.board:
            row=''
            for j in range(self.board_size):
                if i[j]==1:
                    row+="  "
                else:
                    row+=str(i[j])+" "
            print(row)


    def get_next_state(self,move):
        board=self.board
        self.make_a_move(move)
        return_board=self.board
        self.board=board
        return move,return_board

    def get_next_states(self):
        state=[]
        for i in self.posible_moves():
            state.append(self.get_next_state(i))
        return state 
    #Get the state of the game 
    def get_state(self):
        return_board=[]
        new_board=self.board.reshape(self.board_size**2)
        for i in new_board:
            if i!=0:
                return_board.append(math.log2(i))
            else:
                return_board.append(i)
        return_board=np.array(return_board)
        return (return_board/max(return_board)).reshape(self.board_size**2)

    def get_state_predict(self):
        return self.board.reshape(1,self.board_size**2)

    """
    Create a variable that give a procent for spaw of a piece 80% for a 2 and 20% for a 4 
    Get random values for i,j and check if it's in bounderies and if it's a free place
    than place it, else retry
    """ 
    def spawn_new_piece(self):
        change_piece= rand.randint(0,100)
        if(change_piece<=80):
            piece=1
        else:
            piece=2
        counter=1
        i=rand.randint(0,self.board_size-1)
        j=rand.randint(0,self.board_size-1)
        while counter!=0:
            if(self.check_in_board(i,j)==True and self.board[i][j]==0):
                self.board[i][j]=piece*2
                counter-=1
            i=rand.randint(0,self.board_size-1)
            j=rand.randint(0,self.board_size-1)

    def make_a_move(self,direction):
        ''' "0" -> up \n
            "1" -> right \n
            "2" -> down \n
            "3" -> left \n
            return next state and if the game is over or not 
        '''
        # print(direction)
        valid_move=True
        if(self.check_valid_move(direction)!=False):
            reward=0
            self.max_invalid=0
            if(direction==0):
                #up
                # print("UP")
                for j in range (self.board_size):
                    for i in range(1,self.board_size):
                        if(self.board[i][j]!=0 and self.board[i][j]!=1  and i!=0 and self.board[i-1][j]!=1 ):
                            newPozI=i-1
                            '''While you it can move to a specific direction move  '''
                            while (
                                self.board[newPozI][j]==0 and \
                                self.board[newPozI][j]!=1 and \
                                newPozI>0
                                ):
                                newPozI-=1
                            ''' If it hits something verifi if it's same number piece, out of the table or wall '''
                            if self.board[i][j]==self.board[newPozI][j]:
                                self.board[newPozI][j]*=2
                                reward+=self.board[newPozI][j]
                                self.board[i][j]=0
                            elif self.board[newPozI][j]==0:
                                self.board[newPozI][j]=self.board[i][j]
                                self.board[i][j]=0
                            else:
                                if newPozI+1!=i:
                                    self.board[newPozI+1][j]=self.board[i][j]
                                    self.board[i][j]=0
            elif(direction==1):
                #right
                # print("RIGHT")
                for i in range(self.board_size):
                    for j in range (self.board_size-2,-1,-1):
                        if(self.board[i][j]!=0 and self.board[i][j]!=1 and self.board[i][j+1]!=1 and j!=self.board_size-1):
                            newPozJ=j+1
                            while (
                                self.board[i][newPozJ]==0 and \
                                self.board[i][newPozJ]!=1 and\
                                newPozJ<self.board_size-1
                                ):
                                newPozJ+=1
                            if self.board[i][newPozJ]==self.board[i][j]:
                                self.board[i][newPozJ]*=2
                                reward+=self.board[i][newPozJ]
                                self.board[i][j]=0
                            elif self.board[i][newPozJ]==0:
                                self.board[i][newPozJ]=self.board[i][j]
                                self.board[i][j]=0
                            else:
                                if newPozJ-1!=j:
                                    self.board[i][newPozJ-1]=self.board[i][j]
                                    self.board[i][j]=0
            elif direction==2:
                #down
                # print("DOWN")
                for j in range (self.board_size):
                    for i in range(self.board_size-2,-1,-1):
                        if(self.board[i][j]!=0 and self.board[i][j]!=1 and self.board[i+1][j]!=1 ):
                            newPozI=i+1
                            # print("This is the element ",self.board[i][j],i,j)
                            while (
                                self.board[newPozI][j]==0 and\
                                self.board[newPozI][j]!=1 and \
                                newPozI<self.board_size-1
                                ):
                                newPozI+=1
                            if self.board[i][j]==self.board[newPozI][j]:
                                self.board[newPozI][j]*=2
                                reward+=self.board[newPozI][j]
                                self.board[i][j]=0
                            elif self.board[newPozI][j]==0:
                                self.board[newPozI][j]=self.board[i][j]
                                self.board[i][j]=0
                            else:
                                if newPozI-1!=i:
                                    self.board[newPozI-1][j]=self.board[i][j]
                                    self.board[i][j]=0
            elif direction==3:
                # print("LEFT")
                for i in range(self.board_size):
                    for j in range (1,self.board_size):
                        if(self.board[i][j]!=0 and self.board[i][j]!=1  and j!=0 and self.board[i][j-1]!=1 ):
                            newPozJ=j-1
                            # print("This is the element ",self.board[i][j],i,j)
                            while (
                                self.board[i][newPozJ]==0 and\
                                self.board[i][newPozJ]!=1 and \
                                newPozJ>0
                                ):

                                newPozJ-=1
                            if self.board[i][newPozJ]==self.board[i][j]:
                                self.board[i][newPozJ]*=2
                                reward+=self.board[i][newPozJ]
                                self.board[i][j]=0
                            elif self.board[i][newPozJ]==0:
                                self.board[i][newPozJ]=self.board[i][j]
                                self.board[i][j]=0
                            else:
                                if newPozJ+1!=j:
                                    self.board[i][newPozJ+1]=self.board[i][j]
                                    self.board[i][j]=0
            if valid_move==True:    
                self.spawn_new_piece()
            self.score+=reward
            game_over=False
            if len(self.posible_moves())==0:
                game_over=True
            return reward,game_over
        else:
            self.max_invalid+=1
            if(self.max_invalid==10):
                return -4,True
            else:
                return -2,False
    def get_score(self):
        return self.score

    def posible_moves(self):
        moves=[]
        found1=True
        found2=True
        for j in range(self.board_size):
            if(found1==True):
                for i in range(1,self.board_size-1):
                    if (self.board[i][j]==self.board[i+1][j] or self.board[i][j]==self.board[i-1][j])\
                        and self.board[i][j]!=1 or self.board[i][j]==0 or self.board[i+1][j]==0 or self.board[i-1][j]==0 :
                        moves.append(0)
                        moves.append(2)
                        found1=False
                        break
            else:
                break
        for i in range(self.board_size):
            if(found2==True):
                for j in range(1,self.board_size-1):
                    if (self.board[i][j]==self.board[i][j+1] or self.board[i][j]==self.board[i][j-1])\
                        and self.board[i][j]!=1 or self.board[i][j]==0 or self.board[i][j+1]==0 or self.board[i][j-1]==0:
                        moves.append(1)
                        moves.append(3)
                        found2=False
                        break
            else:
                break
        return sorted(moves)
    
    def check_valid_move(self,move):
        if move in self.posible_moves():
            return True
        else :
            return False

    def check_in_board(self, i,j):
        if((i<self.dim-1 or i>=self.board_size-self.dim+1) and (j>self.dim-1 and j<self.board_size-self.dim )):
            return False
        elif((i>self.dim-1 and i<self.board_size-self.dim ) and (j<self.dim-1 or j>=self.board_size-self.dim+1)):
            return False
        return True 

'''
Posible moves test
'''
# env.print_board()
# env.board[0][:]=2
# env.board[1][:]=4
# env.board[2][:]=8
# env.board[3][:]=16

# env.board=np.array([
#     [8,32,2,8],
#     [2,64,8,2],
#     [16,8,32,16],
#     [2,2,4,0]
# ])

''' For random moves play'''