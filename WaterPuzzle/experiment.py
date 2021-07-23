"""
@DATE: 2021/7/14
@Author: Ziqi Wang
@File: experiment.py
"""
import sys

sys.path.append('../')

from WaterPuzzle.waterpuzzle import WaterPuzzle
from WaterPuzzle.agent import QLearningAgent

if __name__ == '__main__':
    game = WaterPuzzle('./levels/2.txt')
    Q_agent = QLearningAgent(game.number_states())
    max_epoch = 100
    for it in range(max_epoch):
        Q_agent.epsilon = (max_epoch - it) / max_epoch
        print(game.run(False, Q_agent))
        game.__init__('./levels/2.txt')

    game.__init__('./levels/2.txt')
    Q_agent.epsilon = 0
    Q_agent.train = False
    res = game.run(True, Q_agent)
