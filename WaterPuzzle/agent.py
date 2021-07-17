"""
@DATE: 2021/7/10
@Author: Ziqi Wang
@File: agent.py
"""

import random
import numpy as np


class QLearningAgent:
    def __init__(self, number_states):
        self.Q_table = np.zeros([number_states, 4])
        self.epsilon = 0.8
        self.learning_rate = 0.8
        self.discount_factor = 0.9
        self.train = True
        self.got_key = 0
        self.action = 0

    def load(self, file_path):
        self.Q_table = np.load(file_path)

    def save(self, file_path):
        np.save(file_path, self.Q_table)

    def make_decision(self, obs_hash: int) -> int:
        if random.uniform(0, 1)<self.epsilon:
            i = random.randint(0,3)
            while self.Q_table[obs_hash][i] != np.max(self.Q_table[obs_hash]):
                i = random.randint(0,3)
            self.action = i
        else:
            self.action = random.randint(0,3)
        return self.action

    def update_Q(self, reward, last_obs, action, new_obs):
        last_q = self.Q_table[last_obs][action]
        new_q = reward + self.discount_factor * np.max(self.Q_table[new_obs])
        self.Q_table[last_obs][action] += self.learning_rate * (new_q - last_q)

