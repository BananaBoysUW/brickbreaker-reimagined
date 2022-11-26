import pygame
import json

from Brick import Brick


class Bricks(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, starting_pos_ratio, bg_color):
        super(Bricks, self).__init__()
        self.width = screen_width
        self.height = screen_height * starting_pos_ratio
        self.bg_color = bg_color

        self.brick_list = self.get_bricks()

        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.surface.get_rect()

        self.render()

    def get_bricks(self):
        with open("rects.json", "r") as f:
            rects = json.load(f)
            brick_list = [Brick(*rect[0], color=rect[1]) for rect in rects]

            return brick_list

    def render(self):
        self.surface.fill(self.bg_color)

        for brick in self.brick_list:
            self.surface.blit(brick.surface, brick.rect)

    def remove_brick(self, brick):
        self.brick_list.remove(brick)

    def update(self):
        self.render()
