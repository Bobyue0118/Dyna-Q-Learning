import numpy as np
import pandas as pd
import math

class Agent:
    ### START CODE HERE ###

    # 初始化时，传入actions参数；epsilon是精度
    def __init__(self, actions, alpha=0.1, gamma=0.7, epsilon=1):
        self.actions = actions
        self.alpha   = alpha                              # learning_rate
        self.gamma   = gamma                              # reward_decay
        self.epsilon = epsilon
        self.qTable  = pd.DataFrame(columns=self.actions) # tabular q-value
        self.cTable  = pd.DataFrame(columns=self.actions) # tabular counter value

    def choose_action(self, observation):
        self.state_exist(observation)

        # tune epsilon
        self.epsilon = 0.01

        # epsilon-greedy method
        if np.random.uniform() < self.epsilon:
            # random
            action = np.random.choice(self.actions)
        else:
            # get all potential actions
            action_to_be = self.qTable.loc[observation]
            # if more than one
            action = np.random.choice(action_to_be[action_to_be == max(action_to_be)].index)

        return action

    def learn(self, s, a, r, s_, done):
        k = 1

        self.state_exist(s_)

        q_predict = self.qTable.loc[s, a]

        if not done:
            q_target = r + self.gamma * max((self.qTable.loc[s_] + k / (1+self.cTable.loc[s_].sum())))
        else:
            q_target = r

        self.cTable.loc[s, a] += 1
        self.qTable.loc[s, a] += self.alpha * (q_target - q_predict)

    def state_exist(self, state):
    # if state not exist, initialize all 0
        if state not in self.qTable.index:
            self.qTable = self.qTable.append(pd.Series(
                [0]*len(self.actions),
                index=self.qTable.columns,
                name=state))

        if state not in self.cTable.index:
            self.cTable = self.cTable.append(pd.Series(
                [0]*len(self.actions),
                index=self.cTable.columns,
                name=state))

class Model:
    '''
    Model(s,a) is utilized to implement model-based RL:
    1. Learn from interaction
    2. Update Q(s,a) after each learning process
    '''
    def __init__(self, actions):
        self.actions = actions
        self.storage = pd.DataFrame(columns=actions, dtype=np.object)

    def store_transition(self, s, a, r, s_):
        if s not in self.storage.index:
            self.storage = self.storage.append(
                pd.Series([None] * len(self.actions),
                index = self.storage.columns,
                name = s)
            )

        self.storage.loc[s, a] = (r, s_)

    def sample_s_a(self):
        s = np.random.choice(self.storage.index)
        a = np.random.choice(self.storage.loc[s].dropna().index)
        return s, a

    def get_r_s_(self, s, a):
        r, s_ = self.storage.loc[s, a]
        return r, s_

# global variables storing last iteration's information
np.random.seed(100)
    ### END CODE HERE ###