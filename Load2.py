from Game import Game_2048
from Agent import Agent
import numpy as n
from tqdm import tqdm
env= Game_2048(4)
agent=Agent(16,True,"./models/After_0_episods.m5")
done=False
env.reset()
best_score=[]
boards=[]
for i in tqdm(range(100)):
    env.reset()
    while not done:
        # current_state=env.get_state()
        # predict=agent.get_qs(current_state)[0]
        # moves=env.possible_moves()
        # for i in range(0,4):
        #     if i not in moves:
        #         predict[i]=float('-inf')
        # action=n.argmax(predict)


        states=env.get_next_states()
        predict_states=[]
        for i in states:
            predict_states.append(agent.get_qs(i[0]))
        action=states[n.argmax(predict_states)][1]
        new_state,score,done=env.playNN(action)
        # print(predict)
        # print(action)
    # print(env.board)
    # print('\n')
    best_score.append(env.get_score())
    boards.append(env.board)
    # print(i)


best_score=n.array(best_score)
boards=n.array(boards)
count=0
for i in boards:
    if 256 in i:
        count+=1

poz=best_score.argmax()
print(best_score[poz])
print(boards[poz])
print(count)