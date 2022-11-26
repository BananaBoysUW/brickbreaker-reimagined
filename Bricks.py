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

    def ltrb_rect_to_points(self, rects):
        rects_as_points = []
        for rect in rects:
            (l, t, r, b), color = rect
            rects_as_points.append((((l, t), (r, t), (r, b), (l, b)), color))

        return rects_as_points

    def get_bricks(self):
        with open("rects.json", "r") as f:
            rects = json.load(f)
            rects = self.ltrb_rect_to_points(rects)
            brick_list = [Brick(rect[0], color=rect[1]) for rect in rects]

            return brick_list

    def render(self):
        self.surface.fill(self.bg_color)

        for brick in self.brick_list:
            pygame.draw.polygon(self.surface, brick.color, brick.points)

    def remove_brick(self, brick):
        self.brick_list.remove(brick)

    def update(self):
        self.render()
