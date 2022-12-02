import pygame
import numpy as np
import utils


class Brick(pygame.sprite.Sprite):
    def __init__(self, points, color):
        super(Brick, self).__init__()

        self.points = points
        self.color = color

        self.zone_numbers = []

        self.lines = utils.points_to_lines(points)

        left, top, width, height = self.get_rect_vals()

        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = pygame.draw.polygon(self.image, self.color, [(x - left, y - top) for x, y in self.points])
        self.rect.update(left, top, width, height)

    def toJSON(self):
        return [self.points, self.color]

    def get_rect_vals(self):
        x_vals, y_vals = [arr.flatten().tolist() for arr in np.split(np.array(self.points), 2, 1)]

        left = min(x_vals)
        top = min(y_vals)
        width = max(x_vals) - left
        height = max(y_vals) - top

        return [left, top, width, height]

    def add_zone_number(self, zone_number):
        if zone_number not in self.zone_numbers:
            self.zone_numbers.append(zone_number)
