from Game import Game_2048
import math

def expectimax(game,depth=2,max_depth=2,base_num=2,rows=4,cols=4,a1=-float('inf'),a2=-float('inf'),a3=-float('inf'),a4=-float('inf')):
    if depth==0:
        # return evaluation(game.board)
        return game.eval()
    else :
        for move in range(4):
            clone_game=game.clone()

            if move==0 and move in game.possible_moves():
                clone_game.move_board(move)
                possible_positions=clone_game.get_free_squares()
                if possible_positions!=None:
                    for row,col in possible_positions:
                        new_clone=clone_game.clone()
                        new_clone.board[row][col]=base_num
                        val1=expectimax(new_clone,depth=depth-1,max_depth=max_depth)
                        a1=max(val1,a1)
            elif move==1  and move in game.possible_moves():
                clone_game.move_board(move)
                possible_positions=clone_game.get_free_squares()
                if possible_positions!=None:
                    for row,col in possible_positions:
                        new_clone=clone_game.clone()
                        new_clone.board[row][col]=base_num
                        val2=expectimax(new_clone,depth=depth-1,max_depth=max_depth)
                        a2=max(val2,a2)
            elif move==2 and move in game.possible_moves():
                clone_game.move_board(move)
                possible_positions=clone_game.get_free_squares()
                if possible_positions!=None:
                    for row,col in possible_positions:
                        new_clone=clone_game.clone()
                        new_clone.board[row][col]=base_num
                        val3=expectimax(new_clone,depth=depth-1,max_depth=max_depth)
                        a3=max(val3,a3)
            elif move==3 and move in game.possible_moves():
                clone_game.move_board(move)
                possible_positions=clone_game.get_free_squares()
                if possible_positions!=None:
                    for row,col in possible_positions:
                        new_clone=clone_game.clone()
                        new_clone.board[row][col]=base_num
                        val4=expectimax(new_clone,depth=depth-1,max_depth=max_depth)
                        a4=max(val4,a4)
        maxVal=max(a1,a2,a3,a4)
        if depth==max_depth:
            dict=[
                [a1,0],
                [a2,1],
                [a3,2],
                [a4,3],   
            ]
            for i in dict:
                if i[0]==maxVal:
                #  and i[1] in game.possible_moves():
                    return maxVal,i[1]
    return maxVal

def highestNumLocation(board):
    #atm this is keeping the largest number at the top left
    rows = len(board)
    cols = len(board[0])
    topLeft = board[0][0]
    for row in range(rows):
        for col in range(cols):
            curNum = board[row][col]
            if curNum > topLeft:
                return -1
    return 1

def emptySquares(board):
    #bonus to more empty squares to ENCOURAGE merging
    rows = len(board)
    cols = len(board[0])
    count = 1
    for row in range(rows):
        for col in range(cols):
            curNum = board[row][col]
            if curNum == 0:
                count *= 1.1 # increase bonus by a ratio
    return count

# this heuristics idea is adopted from:
# https://stackoverflow.com/questions/22342854/what-is-the-optimal-algorithm-for-the-game-2048/23853848#
def findMaxNumAndPos(board):
    # the lowest maxNum is guaranteed to be 2, which is > -1
    targetRow = 0
    targetCol = 0

    rows = len(board)
    cols = len(board[0])
    maxNum = -1
    for row in range(rows):
        for col in range(cols):
            curNum = board[row][col]
            if curNum > maxNum:
                maxNum = curNum
                targetRow = row
                targetCol = col
    return maxNum, targetRow, targetCol

# ideas refined by https://github.com/Kulbear/endless-2048/blob/master/agent/minimax_agent.py
def monotinicity(board):
    # bonus for making rows/cols either strictly decreasing from the left cornor
    bonus = 1
    rows = len(board)
    cols = len(board[0])
    # for every row, check if strictly decreasing from left to right
    for row in range(rows):
        temp = 1
        for col in range(cols-1):
            curNum = board[row][col]
            nextNum = board[row][col+1]
            if curNum > nextNum:
                temp = 1.5
            else:
                temp = 1
        bonus *= temp
    #for every col, check if strictly decreasing from up to down
    for col in range(cols):
        temp = 1
        for row in range(rows-1):
            curNum = board[row][col]
            nextNum = board[row+1][col]
            if curNum > nextNum:
                temp = 1.5
            else:
                temp = 1
        bonus *= temp
    return bonus

# this heuristics idea is also adopted from:
# https://stackoverflow.com/questions/22342854/what-is-the-optimal-algorithm-for-the-game-2048/23853848#
# idea refined by https://github.com/Kulbear/endless-2048/blob/master/agent/minimax_agent.py
def smoothness(board):
    # measures the difference between neighboring tiles and tries to minimize this count
    score = 1
    rows = len(board)
    cols = len(board[0])
    for row in range(rows):
        for col in range(0, cols, 2): # skip a col because we already check all 4 adjacent tiles, more efficient
            curNum = board[row][col]
            for r,c in [(0,1),(1,0),(0,-1),(-1,0)]:
                if rows > row+r >= 0 and cols > col+c >= 0 and curNum != 0:
                    checkedNum = board[row+r][col+c]
                    if curNum-checkedNum != 0:
                        score += math.log(abs(curNum - checkedNum),10) # best way to make large differences small, by using log10
    return score

# idea from https://github.com/Kulbear/endless-2048/blob/master/agent/minimax_agent.py
# and from https://github.com/SrinidhiRaghavan/AI-2048-Puzzle/blob/master/Helper.py
# WEIGHT_MATRIX = [[2048, 1024, 64, 32],[512, 128, 16, 2],[256, 8, 2, 1],[4, 2, 1, 1]] for 2048 specifically
def getMatrix(rows, cols):
    # create a gradiantMatrix based on the current row and cols of the board, so the diagonal is not always all 0!
    gradientMatrix = [ [0]*cols for row in range(rows) ]
    for row in range(rows):
        for col in range(cols):
            if row == 0:
                gradientMatrix[row][col] = cols - col - row #first row, last weight is 0
            else:
                gradientMatrix[row][col] = 0 - col - row # minimize weights of middle rows
    return gradientMatrix

def gradient(board):
    score = 0
    rows = len(board)
    cols = len(board[0])
    # recrate gradiantMatrix based on the current row and cols of the board, so the diagonal is not always all 0!
    gradientMatrix = getMatrix(rows, cols)
    # now compute the score
    for row in range(rows):
        for col in range(cols):
            curNum = board[row][col]
            if curNum != 0:
                score += math.log(curNum,10)*gradientMatrix[row][col] # use log of the tile num so the score is not crazy large
    return score

# Weight Matrix Theories from: https://codemyroad.wordpress.com/2014/05/14/2048-ai-the-intelligent-bot/
# and from http://www.randalolson.com/2015/04/27/artificial-intelligence-has-crushed-all-human-records-in-2048-heres-how-the-ai-pulled-it-off/
# and extremely helpful from https://github.com/Kulbear/endless-2048/blob/master/agent/minimax_agent.py
def evaluation(board):
    # input variables from evaluation functions, so our x1,x2,x3, etc.
    xL = highestNumLocation(board)
    xES = emptySquares(board)
    xMono = monotinicity(board)
    xSmooth = smoothness(board)
    xGrad = gradient(board)
    # print(xL, xES, xMono, xSmooth, xGrad)

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
    val =wLocation*(xL + bias1) + wEmptySquare*(xES + bias2) + \
            wMono*(xMono + bias3) + wSmooth*(xSmooth + bias4) + wGrad*(xGrad + bias5)
    # print(val)
    return val
