"""
@DATE: 2021/7/14
@Author: Ziqi Wang
@File: experiment.py
"""

from waterpuzzle import WaterPuzzle
from agent import QLearningAgent

if __name__ == '__main__':
    Q_table = None
    for _ in range(50):
        game = WaterPuzzle('./levels/1.txt')
        Q_agent = QLearningAgent(game.number_states())
        if Q_table is not None:
            Q_agent.Q_table = Q_table
        print(game.run(False, Q_agent))
        Q_table = Q_agent.Q_table

