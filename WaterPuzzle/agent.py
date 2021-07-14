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
        self.epsilon = 1.0
        self.train = True
        self.got_key = 0
        self.action = 0

    def load(self, file_path):
        self.Q_table = np.load(file_path)

    def save(self, file_path):
        np.save(file_path, self.Q_table)

    def make_decision(self, obs_hash: int) -> int:
        return self.action

    def update_Q(self, reward):
        pass
