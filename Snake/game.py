"""
@DATE: 2021/7/10
@Author: Ziqi Wang
@File: game.py
"""

import pygame
import threading
import random

from common import Directions
from Snake.logic import GameWorld
from Snake.render import AssetMgr, WindowRenderer


class Game:
    max_level = 5

    def __init__(self, render=True, log=False, agent=None):
        assert render or agent, 'The window must be rendered when the mode is human play'
        self.world = GameWorld()
        if render:
            AssetMgr.load()
            pygame.font.init()
            self.renderer = WindowRenderer()
        else:
            self.renderer = None
        self.agent = agent
        self.level = 0
        self.score = 0
        self.log = log

    def update(self):
        self.world.update()
        if self.renderer:
            snake = self.world.snake
            self.renderer.render(
                self.world, level=self.level, score=self.score,
                length=len(snake.dire_queue) + 1
            )

    def on_userevent(self, event):
        """ Deal with custom events """
        if event.name == 'got bean':
            self.score += 20 + 10 * self.level
            self.world.bean_countdown = 0
        """ ----------------------- """

    def run(self):
        if self.renderer:
            self.__run_with_render()
        else:
            return self.__run_simulation()

    def __run_with_render(self):
        clk = pygame.time.Clock()
        frame_count = 0
        step_count = 0
        frame_period = 20 - 2 * self.level  # how many ticks one frame
        while True:  # main loop
            # Keep a high fps, otherwise there will be a key express event lag
            clk.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif not self.agent and event.type == pygame.KEYUP:
                    """ Deal with key input """
                    snake = self.world.snake
                    if event.key == pygame.K_UP and snake.direction != Directions.DOWN:
                        snake.direction = Directions.UP
                    elif event.key == pygame.K_DOWN and snake.direction != Directions.UP:
                        snake.direction = Directions.DOWN
                    elif event.key == pygame.K_LEFT and snake.direction != Directions.RIGHT:
                        snake.direction = Directions.LEFT
                    elif event.key == pygame.K_RIGHT and snake.direction != Directions.LEFT:
                        snake.direction = Directions.RIGHT
                    """ ------------------- """
                    pass
                elif event.type == pygame.USEREVENT:
                    self.on_userevent(event)

            if self.world.finish:
                self.renderer.render_game_over()
                pygame.display.flip()
                continue

            if frame_count % frame_period == 0:
                if self.agent:
                    snake = self.world.snake
                    direction = Directions(0)
                    if frame_count > 0:
                        direction = Directions(t.get_result())

                    t = AgentThread(target=self.agent.make_decision,
                                    args=(self.world, (1000 * frame_period) // 60))  # the thread to make decision
                    t.start()
                    if direction is None:
                        direction = 0
                    if not Directions.exlude(direction, snake.direction):
                        snake.direction = direction
                self.update()
                pygame.display.flip()
                step_count += 1
            if frame_count % 2400 == 2399 and self.level < Game.max_level:
                self.level += 1
                frame_period = 20 - 2 * self.level

            if self.log and step_count % 50 == 49:
                print(
                    'Step %d, Score: %d, Snake Length: %d' %
                    (step_count + 1, self.score, len(self.world.snake))
                )
            frame_count += 1

    def __run_simulation(self):
        # Initialize pygame module to get event supports
        pygame.init()
        step_count = 0
        while True:  # main loop
            # Keep a high fps, otherwise there will be a key express event lag
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT:
                    self.on_userevent(event)
            if self.world.finish:
                break

            snake = self.world.snake
            direction = Directions(self.agent.make_decision(self.world, 100))
            if not Directions.exlude(direction, snake.direction):
                snake.direction = direction
            self.update()

            if self.log and step_count % 50 == 49:
                print(
                    'Step %d, Score: %d, Snake Length: %d' %
                    (step_count + 1, self.score, len(self.world.snake))
                )
            step_count += 1
        return {'steps': step_count, 'score': self.score, 'length': len(self.world.snake)}


class AgentThread(threading.Thread):
    def __init__(self, target, args=()):
        super(AgentThread, self).__init__()
        self.target = target
        self.args = args

    def run(self):
        self.result = self.target(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception:
            print('Agent has not returned the action.')
            return random.randrange(4)
