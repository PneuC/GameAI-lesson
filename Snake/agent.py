"""
@DATE: 2021/7/10
@Author: Ziqi Wang
@File: agent.py
"""
import random
from abc import abstractmethod


class Agent:
    @abstractmethod
    def make_decision(self, observation):
        pass


class RandomAgent(Agent):
    def __init__(self, action_itv=4):
        self.action_itv = action_itv
        self.action = 0
        self.step_count = 0

    def make_decision(self, observation):
        if self.step_count % self.action_itv == 0:
            self.action = random.randrange(4)
        self.step_count += 1
        return self.action


class EvolutionAgent(Agent):
    def __init__(self):
        pass

    def make_decision(self, observation):
        """ Implement it. Note: the Agent shouldn't use GameWorld.update() during evaluation.
        """
        pass
