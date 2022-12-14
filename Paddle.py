import pygame
from Vector2D import Vector2D
import utils


class Paddle(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, width, height, color):
        super(Paddle, self).__init__()

        self.width = width
        self.height = height
        self.color = color

        self.initial_pos = Vector2D(screen_width / 2, screen_height - self.height)
        self.pos = self.initial_pos.copy()
        self.min_x = 0
        self.max_x = screen_width - self.width

        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = pygame.draw.rect(self.surface, self.color, (0, 0, self.width, self.height))

        self.reset_pos()

    def lines(self):
        l, t = self.rect.topleft
        r, b = self.rect.bottomright
        return utils.ltrb_rect_to_lines((l, t, r, b))

    def midpoint(self):
        return self.pos.x + (self.width / 2)

    def update_pos(self):
        self.rect.update(self.pos.x, self.pos.y, self.width, self.height)

    def reset_pos(self):
        self.pos = self.initial_pos.copy()
        self.update_pos()

    def update(self, new_x):
        self.pos.x = utils.map_val(0, 100, self.min_x, self.max_x, new_x)
        self.update_pos()
