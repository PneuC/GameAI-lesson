"""
@DATE: 2021/7/14
@Author: Ziqi Wang
@File: experiment.py
"""

from Waterpuzzle.waterpuzzle import WaterPuzzle
from Waterpuzzle.agent import QLearningAgent

if __name__ == '__main__':
    for _ in range(10):
        game = WaterPuzzle('./levels/1.txt')
        print(game.run(False, QLearningAgent(game.number_states())))

