import numpy as n
import random as r
import copy
import math
# WEIGHT_MATRIX = n.array([
#     [4, 5, 6, 7],
#     [3, 4, 5, 6],
#     [2, 3, 4, 5],
#     [1, 2, 3, 4]
# ])

WEIGHT_MATRIX = n.array([
    [13, 14, 15, 16],
    [9, 10, 11, 12],
    [5, 6, 7, 8],
    [1, 2, 3, 4]
])

# WEIGHT_MATRIX = n.array([
#     [13, 14, 15, 16],
#     [12, 11, 10, 9],
#     [5, 6, 7, 8],
#     [4, 3, 2, 1]
# ])


class Game_2048:
    def __init__(self, size):
        self.size = size
        self.reset()

    def reset(self):
        self.board = n.array([[0 for _ in range(self.size)]
                              for __ in range(self.size)])
        for _ in range(2):
            self.spawn_new_piece()
        self.score = 0

    def get_free_squares(self):
        free_squares = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    free_squares.append([i, j])
        # if free_squares==NoneType:
        if free_squares == []:
            return None
        return free_squares

    def spawn_new_piece(self):
        spaces = self.get_free_squares()
        if(spaces != None):
            i, j = r.choice(spaces)
            self.board[i][j] = 2 if r.random() < 0.9 else 4

    def slide(self, row):
        prev = -1
        new_row = [0, 0, 0, 0]
        i = 0
        row_reward = 0
        for element in row:
            if element != 0:
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
        return new_row, row_reward

    def move_board(self, direction):
        move_reward = 0
        if direction == 3:
            for i in range(self.size):
                self.board[i], reward = self.slide(self.board[i])
                move_reward += reward
        if direction == 0:
            for i in range(self.size):
                self.board[:, i], reward = self.slide(self.board[:, i])
                move_reward += reward
        if direction == 1:
            self.board = n.flip(self.board)
            for i in range(self.size):
                self.board[i], reward = self.slide(self.board[i])
                move_reward += reward
            self.board = n.flip(self.board)
        if direction == 2:
            self.board = n.flip(self.board)
            for i in range(self.size):
                self.board[:, i], reward = self.slide(self.board[:, i])
                move_reward += reward
            self.board = n.flip(self.board)

        return move_reward

    def clone(self):
        return copy.deepcopy(self)

    def possible_moves(self):
        moves = []
        for i in range(4):
            clone_env = self.clone()
            clone_env.move_board(i)
            if n.array_equal(self.board, clone_env.board) == False:
                moves.append(i)
        if moves == []:
            return None
        return moves

    def game_over(self):
        if self.possible_moves() == None:
            return True
        return False

    def play(self, move):
        reward = self.move_board(move)
        self.score += reward
        self.spawn_new_piece()
        return self.game_over()

    def playNN(self,move):
        moves=self.possible_moves()
        if moves!=None:
            if move in moves:
                reward = self.move_board(move)
                self.score += reward
                self.spawn_new_piece()
                # return self.get_state(),self.eval(),self.game_over()
                return self.board.reshape(16),self.eval(),self.game_over()
            else :
                # return self.get_state(),-1000,self.game_over()
                return self.board.reshape(16),-1000,self.game_over()
        else :
            # return self.get_state(),self.eval(),True
            return self.board.reshape(16),self.score(),True

    def get_score(self):
        return self.score

    def penality(self):
        penality = 0
        for i in range(self.size):
            if n.array_equal(self.board[i], sorted(self.board[i])) == False:
                penality += sum(self.board[i])
        for i in range(self.size):
            if n.array_equal(self.board[:, i], n.flip(sorted(self.board[:, i]))) == False:
                penality += sum(self.board[:, i])
        return penality

    def eval(self):
        score = sum(sum(self.board*WEIGHT_MATRIX))
        penality = self.penality()
        return (score-penality)

    def spawn_new_piece_on_poz(self, i, j):
        self.board[i][j] = 2 if r.random() < 0.9 else 4

    def get_state(self):
        board=n.array(self.board)
        board=board.reshape(self.size**2)
        # board=board.reshape(1,self.size**2)
        board=board/board.max()
        return board

    def get_next_states(self):
        moves=self.possible_moves()
        states=[]
        for i in moves:
            states.append(self.next_state(i))
        return states

    def next_state(self,move):
        clone_game=self.clone()
        clone_game.move_board(move)
        return clone_game.board,move,clone_game.eval()

    def best_state(self):
        states=self.get_next_states()
        r_score=-float('inf')
        for board,move,score in states:
            if score>r_score:
                r_score=score
                r_move=move
                r_board=board
        return r_board,r_move,r_score