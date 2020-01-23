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
        return score-penality

    def spawn_new_piece_on_poz(self, i, j):
        self.board[i][j] = 2 if r.random() < 0.9 else 4


class RL(object):
    # similar ideas as above eval function
    def __init__(self, board, rows, cols):
        self.board = board
        self.rows = rows
        self.cols = cols

    # the class arttribute is global to all instance, so it will be aliased ---> learning
    gradientMatrix = [[4-col-row if row ==
                       0 else 0 for col in range(4)] for row in range(4)]

    def updateMatrix(self):
        for row in range(4):
            for col in range(4):
                curNum = self.board[row][col]
                RL.gradientMatrix[row][col] -= 0.1  # penalize every move used
                if curNum != 0:
                    RL.gradientMatrix[row][col] += 0.1 * \
                        math.log(curNum, 10)  # learning rate = 0.1
        print(RL.gradientMatrix)

    def initializeRL():
        # outside the self
        RL.gradientMatrix = [[4-col-row if row ==
                              0 else 0 for col in range(4)] for row in range(4)]

    def evalRL(self):
        # because the gradient matrix is aliased, it will learn as it goes
        xL = highestNumLocation(self.board)
        xES = emptySquares(self.board)
        xMono = monotinicity(self.board)
        xSmooth = smoothness(self.board)

        xGrad = 0
        # now compute the score
        for row in range(4):
            for col in range(4):
                curNum = self.board[row][col]
                if curNum != 0:
                    # use log of the tile num so the score is not crazy large
                    xGrad += math.log(curNum, 10)*RL.gradientMatrix[row][col]

        wLocation = 100
        wEmptySquare = 10
        wMono = 1
        wSmooth = 1
        wGrad = 2

        bias1 = 0
        bias2 = 0
        bias3 = 0
        bias4 = 0
        bias5 = 0
        # be careful with the signs here
        val = wLocation*(xL + bias1) + wEmptySquare*(xES + bias2) + \
            wMono*(xMono + bias3) + wSmooth * \
            (xSmooth + bias4) + wGrad*(xGrad + bias5)
        print(val)
        return val


# env=Game_2048(4)
# # print(env.board)
# # RL(env.board,4,4).updateMatrix()

# while len(env.get_free_squares())>0:
#     env.spawn_new_piece()

# # print(len(env.spawn_new_piece()))
