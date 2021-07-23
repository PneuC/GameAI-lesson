"""
@DATE: 2021/7/10
@Author: Ziqi Wang
@File: render.py
"""

import pygame
from Snake.logic import GameWorld


class AssetMgr:
    background = None
    bean = None
    stone = None
    body = None
    head_sheet = None

    @staticmethod
    def load():
        AssetMgr.background = pygame.image.load('./assets/background.png')
        AssetMgr.bean = pygame.image.load('./assets/bean.png')
        AssetMgr.stone = pygame.image.load('./assets/stone.png')
        AssetMgr.body = pygame.image.load('./assets/body.png')
        head = pygame.image.load('./assets/head_sheet.png')
        AssetMgr.head_sheet = (
            head.subsurface(0, 0, 32, 32),
            head.subsurface(32, 0, 32, 32),
            head.subsurface(64, 0, 32, 32),
            head.subsurface(96, 0, 32, 32)
        )

    @staticmethod
    def head(direction):
        return AssetMgr.head_sheet[direction.value]


class WindowRenderer:
    def __init__(self):
        self.screen = pygame.display.set_mode((1080, 720))
        self.world_renderer = WorldRenderer(self.screen.subsurface(24, 24, 672, 672))
        self.UI_renderer = UIRenderer(self.screen.subsurface(744, 36, 312, 648))

    def render(self, world, **kwargs):
        self.screen.blit(AssetMgr.background, (0, 0))
        self.world_renderer.render(world)
        self.UI_renderer.render(**kwargs)

    def render_game_over(self):
        font = pygame.font.SysFont('comicsansms', 60, bold=True)
        text_surface = font.render('Game Over!', True, (255, 0, 0))
        tar_region = text_surface.get_rect()
        tar_region.center = (360, 360)
        self.screen.blit(text_surface, tar_region)


class WorldRenderer:
    def __init__(self, tar):
        """ create a 2d list that contains all the corresponding
            subsurface for each grid of the game map
        """
        self.tar_grids = [
            [tar.subsurface(32 * j, 32 * i, 32, 32) for j in range(GameWorld.size[1])]
            for i in range(GameWorld.size[0])
        ]
        """ ------------------------------------------------ """

    def render(self, world):
        """ use surface.blit to render the objects """
        game_map = world.game_map
        snake = world.snake
        rows, cols =  world.size
        for i, j in ((c // cols, c % cols) for c in range(rows * cols)):
            if game_map[i][j] == 1:
                if ((i, j) == snake.head_pos).all():
                    self.tar_grids[i][j].blit(AssetMgr.head(snake.direction), (0, 0))
                else:
                    self.tar_grids[i][j].blit(AssetMgr.body, (0, 0))
            elif game_map[i][j] == 2:
                self.tar_grids[i][j].blit(AssetMgr.bean, (0, 0))
            elif game_map[i][j] == 3:
                self.tar_grids[i][j].blit(AssetMgr.stone, (0, 0))
        """ -------------------------------------- """


class UIRenderer:
    def __init__(self, tar):
        self.tar = tar
        self.font = pygame.font.SysFont('comicsansms', 36)

    def render(self, **kwargs):
        level_text = self.font.render(
            'level: %d' % kwargs['level'], True, (0, 0, 0)
        )
        length_text = self.font.render(
            'length: %d' % kwargs['length'], True, (0, 0, 0)
        )
        score_text = self.font.render(
            'score: %d' % kwargs['score'], True, (0, 0, 0)
        )
        self.tar.blit(level_text, (0, 0))
        self.tar.blit(length_text, (0, 40))
        self.tar.blit(score_text, (0, 80))
