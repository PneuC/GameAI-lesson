"""
@DATE: 2021/7/13
@Author: Ziqi Wang
@File: waterpuzzle.py
"""

import pygame

import numpy as np
from common import Directions


class WaterPuzzleRenderer:
    instance = None

    def __init__(self, game_map):
        self.rows, self.cols = game_map.shape
        self.screen = pygame.display.set_mode((self.cols * 24, self.rows * 24))
        WaterPuzzleRenderer.instance = self
        self.grids = [
            [self.screen.subsurface(24 * j, 24 * i, 24, 24) for j in range(self.cols)]
            for i in range(self.rows)
        ]
        self.sheet = {
            'd': pygame.image.load('./assets/door.png'),
            'e': pygame.image.load('./assets/empty.png'),
            'k': pygame.image.load('./assets/key.png'),
            'p': pygame.image.load('./assets/player.png'),
            'w': pygame.image.load('./assets/water.png')
        }

    def render(self, game_map):
        for i in range(self.rows):
            for j in range(self.cols):
                char = game_map[i][j]
                if char != 'w':
                    self.grids[i][j].blit(self.sheet['e'], (0, 0))
                if char != 'k':
                    self.grids[i][j].blit(self.sheet[char], (0, 0))
                else:
                    self.grids[i][j].blit(self.sheet[char], (4, 4))
        pygame.display.flip()


class WaterPuzzle:
    """ Encoding:
        e: empty
        w: water
        p: player
        k: key
        d: door
    """
    def __init__(self, filepath):
        with open(filepath, 'r') as f:
            self.game_map = [list(line[:-1]) for line in f.readlines()]
            self.game_map = np.array(self.game_map)
        self.h, self.w = self.game_map.shape
        self.player_pos = None
        self.check_load()
        self.got_key = False
        self.finish = False

        self.agent = None

    def check_load(self):
        # This method won't check if the key and door are reachable
        key_count = 0
        player_count = 0
        door_count = 0
        h, w = self.game_map.shape
        for i, j in ((c // w, c % w) for c in range(h * w)):
            char = self.game_map[i, j]
            if char == 'k':
                key_count += 1
            if char == 'd':
                door_count += 1
            if char == 'p':
                player_count += 1
                self.player_pos = np.array([i ,j])
        if key_count != 1 or door_count != 1 or player_count != 1:
            return 'There should be exactly 1 key, 1 door and 1 player in the game map'

    def step(self, action):
        next_pos = self.player_pos + Directions(action).vec()
        if not self.pos_valid(next_pos):
            return 0
        reward = 0
        i, j = next_pos
        if self.game_map[i, j] == 'k':
            self.got_key = True
            reward = 5
        if self.game_map[i, j] == 'd':
            reward = 5
            self.finish = True
        self.game_map[i, j] = 'p'
        i, j = self.player_pos
        self.game_map[i, j] = 'e'
        self.player_pos = next_pos
        return reward

    def pos_valid(self, pos):
        if not (0 <= pos[0] < self.h and 0 <= pos[1] < self.w):
            return False
        p = self.game_map[pos[0]][pos[1]] != 'w'
        q = not self.game_map[pos[0]][pos[1]] == 'd' or self.got_key
        return p and q

    def get_obs_hash(self):
        res = self.player_pos[0] * self.w + self.player_pos[1]
        if self.got_key:
            res += self.h * self.w
        return res

    def run(self, render=False, agent=None):
        self.agent = agent
        if render:
            self.__run_with_render()
        else:
            return self.__run_simulation()

    def __run_with_render(self):
        WaterPuzzleRenderer(self.game_map)
        if self.agent:
            self.use_agent()
        while True:  # main loop
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif not self.finish and event.type == pygame.KEYUP :
                if event.key == pygame.K_UP:
                    self.step(0)
                elif event.key == pygame.K_DOWN:
                    self.step(1)
                elif event.key == pygame.K_LEFT:
                    self.step(2)
                elif event.key == pygame.K_RIGHT:
                    self.step(3)
            elif not self.finish and event.type == pygame.USEREVENT:
                last_obs = self.get_obs_hash()
                reward = self.step(event.action)
                if self.agent.train:
                    self.agent.update_Q(reward, last_obs, event.action, self.get_obs_hash())
                pygame.time.wait(200)
                self.use_agent()
            WaterPuzzleRenderer.instance.render(self.game_map)

    def use_agent(self):
        pygame.event.post(
            pygame.event.Event(
                pygame.USEREVENT,
                action=self.agent.make_decision(self.get_obs_hash())
            )
        )

    def __run_simulation(self):
        step_count = 0
        score = 0
        while not self.finish and step_count < 10000:  # main loop
            last_obs = self.get_obs_hash()
            action = self.agent.make_decision(last_obs)
            reward = self.step(action)
            new_obs = self.get_obs_hash()
            self.agent.update_Q(reward, last_obs, action, new_obs)
            score += reward
            step_count += 1
        return {'steps': step_count, 'score': score}

    def number_states(self):
        return self.h * self.w * 2
