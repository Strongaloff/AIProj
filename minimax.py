from Game import Game_2048
import numpy as n
import random
from expectimax import evaluation


def minimax(game, depth=6, max_depth=6, alpha=-float('inf'), beta=float("inf"), maximazing=True):
    if depth <= 0 or game.game_over() == True:
        # return evaluation(game.board)
        return game.eval()
    else:
        if maximazing:
            moves = game.possible_moves()
            if moves != None:
                best_move = moves[0]
                vals = [float("-inf")]*4
                for move in moves:
                    clone_game = game.clone()
                    clone_game.move_board(move)
                    vals[move] = (minimax(clone_game, depth-1,
                                          max_depth, alpha, beta, False))
                    alpha = max(alpha, vals[move])
                    if beta <= alpha:
                        break
                if depth == max_depth:
                    vals = n.array(vals)
                    return alpha, vals.argmax()
            return alpha
        else:
            possible_tiles = game.get_free_squares()
            if possible_tiles != None:

                for i, j in possible_tiles:
                    clone_game = game.clone()
                    clone_game.spawn_new_piece_on_poz(i, j)
                    val = minimax(clone_game, depth-1,
                                  max_depth, alpha, beta, True)
                    beta = min(val, beta)
                    if beta <= alpha:
                        break
                return beta
            else:
                return float("-inf")


game = Game_2048(4)
print(minimax(game))
