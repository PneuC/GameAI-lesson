"""
@DATE: 2021/7/14
@Author: Ziqi Wang
@File: experiment.py
"""
import sys
sys.path.append('../')

from waterpuzzle import WaterPuzzle
from agent import QLearningAgent

if __name__ == '__main__':
    game = WaterPuzzle('./levels/1.txt')
    Q_agent = QLearningAgent(game.number_states())
    max_epoch = 100
    for it in range(max_epoch):
        Q_agent.epsilon = (max_epoch - it) / max_epoch
        print(game.run(False, Q_agent))
        game.__init__('./levels/1.txt')

    game.__init__('./levels/1.txt')
    Q_agent.epsilon = 0
    Q_agent.train = False
    res = game.run(True, Q_agent)
