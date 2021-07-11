"""
@DATE: 2021/7/10
@Author: Ziqi Wang
@File: experiment.py
"""
from agent import RandomAgent
from game import Game


if __name__ == '__main__':
    for _ in range(30):
        print(Game(False, agent=RandomAgent()).run())
