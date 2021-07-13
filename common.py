"""
@DATE: 2021/7/13
@Author: Ziqi Wang
@File: common.py
"""

from enum import Enum
import numpy as np


dire_vecs = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])


class Directions(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

    @staticmethod
    def exlude(dire1, dire2):
        p = dire1.value // 2 == dire2.value // 2
        q = dire1.value % 2 != dire2.value % 2
        return p and q

    def vec(self):
        global dire_vecs
        return dire_vecs[self.value]

if __name__ == '__main__':
    print(Directions.UP.vec())
