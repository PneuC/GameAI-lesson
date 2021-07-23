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
        self.action = random.randint(0, 3)

    def load(self, file_path):
        """
        导入训练好的Q-table
        """
        self.Q_table = np.load(file_path)

    def save(self, file_path):
        """
        保存训练好的Q-table
        """
        np.save(file_path, self.Q_table)

    def make_decision(self, obs_hash: int) -> int:
        """
        epsilon-greedy的方式做出行动。如果不训练，self.epsilon设为0
        """
        if random.uniform(0, 1) < self.epsilon:
            self.action = random.randint(0,3)
        else:
            self.action = self.Q_table[obs_hash].argmax()
        return self.action

    def update_Q(self, reward, last_obs, action, new_obs):
        if not self.train:
            return
        last_q = self.Q_table[last_obs][action]

        # 更新Q-value，还有其他的更新方式吗？
        new_q = reward + self.discount_factor * np.max(self.Q_table[new_obs])
        self.Q_table[last_obs][action] += self.learning_rate * (new_q - last_q)

