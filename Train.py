from Agent import Agent
from Game import Game_2048 as G
import numpy as n
import random as r 
from tqdm import tqdm

def dqn():
    env=G(4)
    agent=Agent(env.size**2)

    NUMBER_OF_EPISODS=20_000
    EPSILON=1
    EPSILON_DECAY=0.000_06
    EPSILON_MIN=0.1
    SAVE_EVERY=1000
    for episod in tqdm(range(NUMBER_OF_EPISODS),):
        env.reset()
        current_state=env.board
        # print(current_state)
        step=1
        done=False
        while not done:
            if r.random()<EPSILON: #Trebuie sa fie rand mai mic ca epsilon sa fie corect
                state=env.best_state()
                action=state[1]
                score=state[2]
            else:
                states=env.get_next_states()
                predict_states=[]
                for i in states:
                    predict_states.append(agent.get_qs(i[0]))
                action=states[n.argmax(predict_states)][1]

            new_state,score,done=env.playNN(action)
            # new_state=env.board

            agent.add_to_memory(n.reshape(current_state,16),new_state,score,done)
            agent.train()
            current_state=new_state
            step+=1
        if EPSILON > EPSILON_MIN:
            EPSILON -= EPSILON_DECAY
            EPSILON = max(EPSILON_MIN, EPSILON)
        if (episod+1)%SAVE_EVERY==0:
            agent.save(int(episod/SAVE_EVERY))  
    # print(agent.get_qs(env.get_state()))

if __name__ == "__main__":
    dqn()
    # env=G(4)
    # # states=n.array(env.get_next_states())
    # states=env.get_next_states()
    # print(max(states))