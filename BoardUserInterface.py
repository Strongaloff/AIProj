import Env as Env
# import Agent_2048 as Agent
import Constants as const
import random as rand
from tkinter import *
from os import system
import time
from multiprocessing import Pool


def clear():
    system("cls")


# episodes = 2000
# max_steps = None
# epsilon_stop_episode = 1500
# mem_size = 20000
# discount = 0.95
# batch_size = 512
# epochs = 1
# render_every = 50
# replay_start_size = 2000
# train_every = 1
# n_neurons = [32, 32]
# render_delay = None
# activations = ['relu', 'relu', 'linear']

boardSize = 2
class GameGrid(Frame):
    def __init__(self):
        self.Environment = Env.Board_2048(boardSize)
        Frame.__init__(self)

        # agent = Agent.Agent(2,
        #                     n_neurons=n_neurons, activations=activations,
        #                     epsilon_stop_episode=epsilon_stop_episode, mem_size=mem_size,
        #                     discount=discount, replay_start_size=replay_start_size)

        self.grid()
        self.master.title('2048')

        self.grid_cells = []
        self.init_grid()
        self.update_grid_cells()
        root = Tk()
        root.update()
        root.withdraw()
        self.Run_Game()
        self.mainloop()

    def init_grid(self):
        if boardSize == 2:
            basedFont = ("Verdana", 40, "bold")
        elif boardSize == 3 or boardSize == 4:
            basedFont = ("Verdana", 20, "bold")
        elif boardSize == 5:
            basedFont = ("Verdana", 10, "bold")

        background = Frame(self, bg=const.BACKGROUND_COLOR_GAME,
                           width=const.SIZE, height=const.SIZE)
        background.grid()

        for i in range(self.Environment.board_size):
            grid_row = []
            for j in range(self.Environment.board_size):
                cell = Frame(background, bg=const.BACKGROUND_COLOR_CELL_EMPTY,
                             width=const.SIZE / self.Environment.board_size,
                             height=const.SIZE / self.Environment.board_size)
                cell.grid(row=i, column=j, padx=const.GRID_PADDING,
                          pady=const.GRID_PADDING)
                t = Label(master=cell, text="",
                          bg=const.BACKGROUND_COLOR_CELL_EMPTY,
                          justify=CENTER, font=basedFont, width=5, height=2)
                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)

    def update_grid_cells(self):
        for i in range(self.Environment.board_size):
            for j in range(self.Environment.board_size):
                new_number = self.Environment.board[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(
                        text="", bg=const.BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(text=str(
                        new_number), bg=const.BACKGROUND_COLOR_DICT[new_number],
                        fg=const.CELL_COLOR_DICT[new_number])
        self.update_idletasks()
# py BoardUserInterface.py

    def Run_Game(self, mode="play"):
        time.sleep(1)
        total_reward = 0
        move = rand.choice(self.Environment.posible_moves())
        self.Environment.print_board()
        reward, game_over = self.Environment.make_a_move(move)
        total_reward += reward
        if mode == "train":
            print(6)
        else:
            while game_over == False:
                clear()
                move = rand.choice(self.Environment.posible_moves())
                self.Environment.print_board()
                reward, game_over = self.Environment.make_a_move(move)
                total_reward += reward
                time.sleep(0.1)
                self.update_grid_cells()
        print('\n')
        self.Environment.print_board()
        print('\n')
        print(total_reward)
        time.sleep(5)
        exit()


gamegrid = GameGrid()
