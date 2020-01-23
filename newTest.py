from Game import Game_2048
import random as r
from expectimax import expectimax
from minimax import minimax
import numpy as n
from tqdm import tqdm
env = Game_2048(4)
done = False
scores = []
boards = []

for _ in tqdm(range(10)):
    env.reset()
    done = False
    while done != True:
        score, move = expectimax(env, depth=2, max_depth=2)
        # score, move = minimax(env)
        if move in env.possible_moves():
            done = env.play(move)
        else:
            done = env.play(r.choice(env.possible_moves()))
        # print("\n")
        # print(env.board)
        # print(score)
    scores.append(env.get_score())
    boards.append(env.board)

scores = n.array(scores)
maxim = scores.argmax()
print(maxim)
print(scores[maxim])
print(boards[maxim])
