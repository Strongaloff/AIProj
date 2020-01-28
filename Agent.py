from keras.models import Sequential,load_model
from keras.layers import Dense
from keras.optimizers import Adam
import random as r 
import numpy as n
from collections import deque
import datetime
REPLAY_MAX_MEMORY=50_000
MIN_REPLAY_MEMORY=1000
MINI_BATCH_SIZE=64
DISCOUNT=0.9
UPDATE_EVERY=1000
class Agent:
    def __init__(self,input_size,load=False,location=""):
        if load==True:
            self.model=load_model(location)
        else:
            self.model=self.create_model(input_size)   

        self.target_model=self.create_model(input_size)
        self.target_model.set_weights(self.model.get_weights())
        self.replay_memory=deque(maxlen=REPLAY_MAX_MEMORY)
        self.target_update_counter=0


    def create_model(self,input_size):
        model=Sequential()
        model.add(Dense(input_size,activation="relu",input_dim=input_size))
        model.add(Dense(256,activation="relu",input_dim=input_size))
        model.add(Dense(64,activation="relu",input_dim=input_size))
        model.add(Dense(1,activation="linear"))
        model.compile(loss='mse',optimizer=Adam(lr=0.0001),metrics=['acc'])
        return model    

    def add_to_memory(self,state,next_state,score,done):
        self.replay_memory.append([state,next_state,score,done])

    def train(self):
        if len(self.replay_memory)<MIN_REPLAY_MEMORY:
            return
        else:
            mini_batch  =r.sample(self.replay_memory,MINI_BATCH_SIZE)

            current_states=n.array([x[1] for x in mini_batch])
            # print(current_states)
            
            current_qs_list=[x[0] for x in self.model.predict(current_states)]
            # print(current_qs_list)
            X=[]
            y=[]
            # current_state,action,new_state,score,done
            for index,(current_state,_,reward,done) in enumerate(mini_batch):

                if not done:
                    new_q=reward+DISCOUNT*current_qs_list[index]

                else:
                    new_q=reward
                    
                X.append(current_state)
                y.append(new_q)

            self.model.fit(
                n.array(X),
                n.array(y),
              batch_size=MINI_BATCH_SIZE,
              epochs=2,
              verbose=0)

            self.target_update_counter+=1

            if self.target_update_counter>UPDATE_EVERY:
                self.target_update_counter=0
                self.target_model.set_weights(self.model.get_weights())

    def get_qs(self,state):
        return self.model.predict(state.reshape(1,16))

    def save(self,name):
        self.model.save("./models/After_"+str(name)+"_episods.m5")