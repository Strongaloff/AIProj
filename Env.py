
import random as r
from os import system
import time
import numpy as n
import math
import copy
def clear():
    system("cls")
#Best
WEIGHT_MATRIX = n.array([
    [4, 5, 6, 7],
    [3, 4, 5, 6],
    [2, 3, 4, 5],
    [1, 2, 3, 4]
])


# WEIGHT_MATRIX = n.array([
#     [6.5, 7, 8, 10],
#     [3, 1, .7, .5],
#     [-2, -1.8, -1.5, -.5],
#     [-3, -3.5, -3.7, -3.8]
# ])
# WEIGHT_MATRIX=n.array([
#     [13 ,14 ,15 ,16 ],
#     [9  ,10 ,11 ,12 ],
#     [5  ,6  ,7  ,8  ],
#     [1  ,2  ,3  ,4  ]
# ])
# WEIGHT_MATRIX=n.array([
#     [13 ,14 ,15 ,16 ],
#     [12  ,11 ,10 ,9 ],
#     [5  ,6  ,7  ,8  ],
#     [4  ,3  ,2  ,1  ]
# ])

# WEIGHT_MATRIX = n.array([
#     [20, 20, 30, 50],
#     [15, 15, 20, 30],
#     [0, 0, 5, 15],
#     [-15, -10, -5, -5]
# ])
WEIGHT_MATRIX2 = [
    [2048, 1024, 64 , 32 ],
    [512 , 128 , 16 , 16 ],
    [256 , 8   , 4  , 2  ],
    [8   , 4   , 2  , 1  ]
]

# WEIGHT_MATRIX = n.array([
#     [8192, 16384 , 32768,65536 ],
# #     [4096,2048 , 1024  , 512 ],
#     [512,1034 , 2048 , 4096 ],
#     [32 ,64   ,128  , 256  ],
#     [2   , 4   , 8  , 16  ]
# ])

class Board_2048:
    
    def __init__(self,board_size ):
        self.dim=board_size
        self.board_size=(board_size*3)-2
        self.reset()

    def reset(self):    
        self.board=n.array([[0 for i in range(self.board_size)] for j in range(self.board_size) ])
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.check_in_board(i,j)==False:
                    self.board[i][j]=1
        self.spawn_new_piece()
        self.spawn_new_piece()
        self.score=0

    def get_free_squares(self):
        free_squares = []
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] == 0:
                    free_squares.append([i, j])

        if free_squares == []:
            return None
        return free_squares

    def get_next_state(self,move):
        clone_game=self.clone()
        clone_game.make_a_move(move)
        return move,clone_game.board

    def get_next_states(self):
        state=[]
        for i in self.posible_moves():
            state.append(self.get_next_state(i))
        return state 
    #Get the state of the game


    """
    Create a variable that give a procent for spaw of a piece 90% for a 2 and 10% for a 4 
    Get random values for i,j and check if it's in bounderies and if it's a free place
    than place it, else retry
    """ 
    def spawn_new_piece(self):
        spaces = self.get_free_squares()
        if(spaces != None):
            i, j = r.choice(spaces)
            self.board[i][j] = 2 if r.random() < 0.9 else 4

    def make_a_move(self,direction):
        move_reward = 0
        if direction == 3:
            for i in range(self.board_size):
                self.board[i], reward = self.slide(self.board[i])
                move_reward += reward
        if direction == 0:
            for i in range(self.board_size):
                self.board[:, i], reward = self.slide(self.board[:, i])
                move_reward += reward
        if direction == 1:
            self.board = n.flip(self.board)
            for i in range(self.board_size):
                self.board[i], reward = self.slide(self.board[i])
                move_reward += reward
            self.board = n.flip(self.board)
        if direction == 2:
            self.board = n.flip(self.board)
            for i in range(self.board_size):
                self.board[:, i], reward = self.slide(self.board[:, i])
                move_reward += reward
            self.board = n.flip(self.board)

        return move_reward
    
    def get_score(self):
        return self.score
    
    def slide(self,row):
        prev = -1
        new_row = [0]*len(row)
        i = 0
        row_reward = 0
        for index, element in enumerate(row):
            if element != 0 and element != 1:
                if prev == -1:
                    prev = element
                    new_row[i] = element
                    i += 1
                elif prev == element:
                    new_row[i-1] = 2*prev
                    row_reward += new_row[i-1]
                    prev = -1
                else:
                    new_row[i] = element
                    prev = element
                    i += 1
            elif element == 1:
                new_row[index] = 1
                i = index+1
                prev=-1
        return new_row, row_reward
    
    def possible_moves(self):
        moves = []
        for i in range(4):
            clone_env = self.clone()
            clone_env.make_a_move(i)
            if n.array_equal(self.board, clone_env.board) == False:
                moves.append(i)
        if moves == []:
            return None
        return moves

    def check_in_board(self, i,j):
        if((i<self.dim-1 or i>=self.board_size-self.dim+1) and (j>self.dim-1 and j<self.board_size-self.dim )):
            return False
        elif((i>self.dim-1 and i<self.board_size-self.dim ) and (j<self.dim-1 or j>=self.board_size-self.dim+1)):
            return False
        return True 

    def clone(self):
        return copy.deepcopy(self)
    
    def game_over(self):
        if self.possible_moves() == None:
            return True
        return False
    
    def play(self,move):
        reward=self.make_a_move(move)
        self.spawn_new_piece()
        return self.game_over()

    # HEURISTIC FUNCTIONS

    def highest_block(self,board):
        maxim=board.argmax()
        i=int(maxim/self.board_size)
        j=maxim%self.board_size
        # return i,j
        if (i,j)==(0,0) or (i,j)==(0,self.board_size) or (i,j)==(self.board_size,0) or (i,j)==(self.board_size,self.board_size):
            return 1000
        else:
            return 0 

    def table_sum(self,board):
        suma=0
        for i in board:
            for j in i:
                if(j!=0 and j!=1):
                    suma+=j
        return suma

    def can_merge(self):
        merge=0
        for i in range(self.board_size):
            for j in range(self.board_size-1):
                if(self.board[i][j]!=0 and self.board[i][j]!=1):
                    k=j+1
                    go=True
                    while k<self.board_size and go:
                        # print("fisrt go ")
                        if self.board[i][k]==0:
                            k+=1
                        elif self.board[i][j]==self.board[i][k]:
                            merge+=1
                            go=False
                        else:
                            go=False

        for i in range(self.board_size):
            for j in range(self.board_size-1):
                if(self.board[j][i]!=0 and self.board[j][i]!=1):
                    k=j+1
                    go=True
                    while k<self.board_size and go:
                        if self.board[k][i]==0:
                            k+=1
                        elif self.board[j][i]==self.board[k][i]:
                            merge+=1
                            go=False
                        else :
                            go=False
        return merge
    
    def monotonicity(self):
        """Monotonicity heuristic tries to ensure that the values of the tiles are all either increasing or decreasing along both the left/right and up/down directions"""
        board = self.board
        mono = 0

        row, col = len(board), len(board[0]) if len(board) > 0 else 0
        for r in board:
            diff = r[0] - r[1]
            for i in range(col - 1):
                if (r[i] - r[i + 1]) * diff <= 0:
                    mono += 1
                diff = r[i] - r[i + 1]

        for j in range(row):
            diff = board[0][j] - board[1][j]
            for k in range(col - 1):
                if (board[k][j] - board[k + 1][j]) * diff <= 0:
                    mono += 1
                diff = board[k][j] - board[k + 1][j]

        return mono

    def smoothness(self):
        """Smoothness heuristic measures the difference between neighboring tiles and tries to minimize this count"""
        board = self.board
        smoothness = 0

        row, col = len(board), len(board[0]) if len(board) > 0 else 0
        for r in board:
            for i in range(col - 1):
                smoothness += abs(r[i] - r[i + 1])
                pass
        for j in range(row):
            for k in range(col - 1):
                smoothness += abs(board[k][j] - board[k + 1][j])

        return smoothness

    def weighted_board(self):
        """Perform point-wise product on the game board and a pre-defined weight matrix"""
        board = self.board

        result = 0
        for i in range(len(board)):
            for j in range(len(board)):
                if(board[i][j]!=0 and board[i][j]!=1):
                    result += board[i][j] * WEIGHT_MATRIX2[i][j]

        # Larger result means better
        return result

    def max_tile_position(self):
        """Return an significantly large negative when the max tile is not on the desired corner, vice versa"""
        board = self.board
        max_tile = max(max(board, key=lambda x: max(x)))

        # Considered with the WEIGHT_MATRIX, always keep the max tile in the corner
        if board[0][self.board_size-1] == max_tile :
            return 10
        else:
            return -10
    
    
    
    def spawn_new_2_on_poz(self,i,j):
        self.board[i][j]=2

    def spawn_new_4_on_poz(self,i,j):
        self.board[i][j]=4
    
    
    def monoton(self):
        score=0
        for i in range(self.board_size):
            order=True
            for j in range(self.board_size-1):
                if self.board[i][j]<=self.board[i][j+1]:
                    order=False
                    break
            if(order==True):
                score+=sum(self.board[i])
            else: 
                score-=max(self.board[i])-min(self.board[i])
        for i in range(self.board_size):
            order=True
            for j in range(self.board_size-1):
                if self.board[j][i]>=self.board[j+1][i]:
                    order=False
                    break
            if(order==True):
                score+=sum(self.board[:,i])
            else: 
                score-=max(self.board[:,i])-min(self.board[:,i])
        return score
    
    def penality(self):
        penality=0
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j]!=0 and self.board[i][j]!=1:
                    if j+1<self.board_size:
                        if self.board[i][j]>self.board[i][j+1]  and self.board[i][j+1]!=0 and self.board[i][j+1]!=1:
                            penality+=abs(self.board[i][j]-self.board[i][j+1])
                    if i+1<self.board_size:
                        if self.board[i][j]<self.board[i+1][j]  and self.board[i+1][j]!=0 and self.board[i+1][j]!=1:
                            penality+=abs(self.board[i][j]-self.board[i+1][j])
                    if i-1>0:
                        if self.board[i][j]>self.board[i-1][j]  and self.board[i-1][j]!=0 and self.board[i-1][j]!=1:
                            penality+=abs(self.board[i][j]-self.board[i-1][j])
                    if j-1>0:
                        if self.board[i][j]<self.board[i][j-1]  and self.board[i][j-1]!=0 and self.board[i][j-1]!=1:
                            penality+=abs(self.board[i][j]-self.board[i][j-1])
        return penality

    def eval(self):
        board=self.board
        heuristiac=[]
        heuristiac.append(self.free_space(board))
        heuristiac.append(self.weighted_board())
        heuristiac.append(self.smoothness())
        heuristiac.append(self.monotonicity())
        heuristiac.append(self.max_tile_position())
        return sum(heuristiac)
        # return heuristiac
    
    def eval_2_0(self):
        heuristic=0
        heuristic+=self.free_space(self.board)
        # heuristic+=int(self.max_tile_position())
        heuristic+=self.weighted_board()
        heuristic+=self.can_merge()
        heuristic+=self.smoothness()
        heuristic-=self.monotonicity()
        # return heuristic
        return heuristic
    
    def eval_3_0(self):
        score=0
        penality=0
        if self.board_size!=4:
            a = n.array([[self.board_size*j+i for i in range(self.board_size)
                          ]for j in range(self.board_size)]
                        )
            WEIGHT_MATRIX = n.flip(n.flip(a), axis=1)

        score = sum(sum(n.dot(self.board, WEIGHT_MATRIX)))
        # score+=self.free_space(self.board)
        # score+=self.can_merge()
        # score+=self.max_tile_position()
        # if self.game_over_function()==True:
        #     penality+=10000
        penality+=self.penality()
        return score-penality
