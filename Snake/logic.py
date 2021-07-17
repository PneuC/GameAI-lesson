"""
@DATE: 2021/7/10
@Author: Ziqi Wang
@File: logic.py
"""

import random
import pygame
import numpy as np

from common import Directions


class Snake:    # 🐍
    def __init__(self, game_map):
        self.dead = False
        self.head_pos = np.array([9, 11])
        self.tail_pos = np.array([13, 11])
        self.direction = Directions.UP
        # Store the diretion of each segment of the snake body to update tail positoin
        self.dire_queue = [Directions.UP] * 4
        # Set snake elements in the game map
        game_map[9:14, 11] = 1

    def update(self, game_map, simulation=False):
        # Update the state of the snake and modify the game map
        """ Please complete the update function """
        # Compute the next postion of the snake head
        res = ''
        next_pos = (self.head_pos + self.direction.vec()) % GameWorld.size
        if game_map[next_pos[0]][next_pos[1]] == 0:
            # next position is empty
            i, j = next_pos
            game_map[i][j] = 1
            i, j = self.tail_pos
            game_map[i][j] = 0
            self.tail_pos = (self.tail_pos + self.dire_queue[-1].vec()) % GameWorld.size
            self.dire_queue.insert(0, self.direction)
            self.dire_queue.pop()

        elif game_map[next_pos[0]][next_pos[1]] in {1, 3}:
            # next position is snake body or stone, game over
            self.dead = True
        elif game_map[next_pos[0]][next_pos[1]] == 2:
            # get bean
            game_map[next_pos[0]][next_pos[1]] = 1
            if not simulation:
                pygame.event.post(pygame.event.Event(pygame.USEREVENT, name='got bean'))
            res = 'got bean'
            # 更新方向队列
            self.dire_queue.insert(0, self.direction)
        if not self.dead:
            self.head_pos = next_pos
        """ ------------------------ """
        return res

    def __len__(self):
        return len(self.dire_queue) + 1


class GameWorld:
    size = (21, 21)
    max_stone_num = 24

    def __init__(self):
        # create a 21 * 21 array to represent the game map
        self.game_map = np.zeros(GameWorld.size, int)
        """ Object Type Table:
            0: empty
            1: snake
            2: bean
            3: stone
        """
        self.snake = Snake(self.game_map)
        self.bean_countdown = 0
        self.stone_countdown = 0
        self.bean_pos = [0, 0]
        self.stone_num = 0
        self.finish = False

    def update_bean(self):
        """ Please complete the logic of updating bean. A suggest form of fresh time funcion is
            (|x_snake - x_bean| + |y_snake - y_bean|) * random(k1, k2) + b, k2 > k1 > 1, b > 1
        """
        if self.bean_countdown <= 0:
            i, j = self.bean_pos
            if self.game_map[i][j] == 2:
                self.game_map[i][j] = 0
            snake_pos = self.snake.head_pos
            i, j = self.gen_rand_empty_pos(5)
            self.game_map[i][j] = 2
            self.bean_pos = [i, j]
            self.bean_countdown = int(abs(snake_pos - (i, j)).sum() * random.uniform(1.5, 2.0) + 5)
        self.bean_countdown -= 1
        """ ------------------------------------------------------------------------------- """
        pass

    def update_stone(self):
        """ Complete the logic of updating stone """
        if self.stone_num >= GameWorld.max_stone_num:
            return
        if self.stone_countdown == 0:
            i, j = self.gen_rand_empty_pos(5)
            self.game_map[i][j] = 3
            self.stone_countdown = random.randrange(30, 50)
        self.stone_countdown -= 1
        """ ----------------------------------- """
        pass

    def gen_rand_empty_pos(self, dis_to_snake_head=0):
        i = random.randrange(0, GameWorld.size[0])
        j = random.randrange(0, GameWorld.size[1])
        while self.game_map[i][j] != 0 or abs(self.snake.head_pos - (i, j)).sum() < dis_to_snake_head:
            i = random.randrange(0, GameWorld.size[0])
            j = random.randrange(0, GameWorld.size[1])
        return i, j

    def update(self):
        self.update_bean()
        self.update_stone()
        self.snake.update(self.game_map)
        if self.snake.dead:
            self.finish = True