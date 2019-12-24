import random as rand
from os import system
import time
def clear():
    system("clear")

class Board_2048:
    def __init__(self,board_size ):
        self.dim=board_size
        self.board_size=(board_size*3)-2
        self.board=[[0 for i in range(self.board_size)] for j in range(self.board_size) ]
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
                print(i,j)
            i=rand.randint(0,self.board_size-1)
            j=rand.randint(0,self.board_size-1)
            val=rand.randint(1,2)
       #for test
        # self.board[3][0]=4
        # self.board[2][0]=2
        # self.board[3][1]=4  
        # self.board[3][2]=2   
        # self.board[3][3]=2   
    def print_board(self):
        for i in self.board:
            row=''
            for j in range(self.board_size):
                if i[j]==1:
                    row+="  "
                else:
                    row+=str(i[j])+" "
            print(row)

    
    def check_game_over(self):
        for row in self.board:
            if 0 in row:
                return False
        for i in range(0,self.board_size-2):
            for j in range(1,self.board_size-2):
                if self.check_brothers(i,j)==True:
                    return False

        return True

    def check_brothers(self,i,j):
        if(
            self.board[i][j]==self.board[i][j+1] or \
            self.board[i][j]==self.board[i][j-1] or \
            self.board[i][j]==self.board[i+1][j] or \
            self.board[i][j]==self.board[i-1][j]):
            return True
        return False

    #Get the state of the game 
    def get_state(self):
        return self.board


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
                # self.board[i][j]=2
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

        if(direction==0):
            #up
            # print("UP")
            for j in range (self.board_size):
                for i in range(1,self.board_size):
                    if(self.board[i][j]!=0 and self.board[i][j]!=1  and i!=0 and self.board[i-1][j]!=1 ):
                        newPozI=i-1
                        while (
                            self.board[newPozI][j]==0 and \
                            self.board[newPozI][j]!=1 and \
                            newPozI>0
                            ):
                            newPozI-=1
                        if self.board[i][j]==self.board[newPozI][j]:
                            self.board[newPozI][j]*=2
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
                            self.board[i][j]=0
                        elif self.board[i][newPozJ]==0:
                            self.board[i][newPozJ]=self.board[i][j]
                            self.board[i][j]=0
                        else:
                            if newPozJ+1!=j:
                                self.board[i][newPozJ+1]=self.board[i][j]
                                self.board[i][j]=0

        if (self.check_game_over() ==True):
            return self.get_state(), True


    def check_in_board(self, i,j):
        if((i<self.dim-1 or i>=self.board_size-self.dim+1) and (j>self.dim-1 and j<self.board_size-self.dim )):
            return False
        elif((i>self.dim-1 and i<self.board_size-self.dim ) and (j<self.dim-1 or j>=self.board_size-self.dim+1)):
            return False
        return True 

env= Board_2048(2)
i=0
env.print_board()
# while i<5:
while env.check_game_over()==False:
    clear()
    env.make_a_move(rand.randint(0,3))
    env.spawn_new_piece()
    env.print_board()
    time.sleep(0.1)
    i+=1