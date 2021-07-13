"""
@DATE: 2021/7/10
@Author: Ziqi Wang
@File: agent.py
"""
import random
from abc import abstractmethod
from copy import deepcopy

from typing import List, Dict

from Snake.logic import GameWorld
from common import Directions


def simulate(world, action_seq: List[int]) -> Dict:
    result = {
        'distance to bean': 0,
        'dead': False,
        'got bean': False
    }
    game_map = world.game_map.copy()
    snake = deepcopy(world.snake)
    for action in action_seq:
        snake.direction = Directions(action)
        res = snake.update(game_map)
        if res == 'got bean':
            result['got bean'] = True
        if snake.dead:
            result['dead'] = True
    result['distance to bean'] = abs(snake.head_pos - world.bean_pos).sum()
    return result

class Agent:
    @abstractmethod
    def make_decision(self, observation: GameWorld) -> int:
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
