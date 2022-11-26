import pygame


class Brick(pygame.sprite.Sprite):
    def __init__(self, left, top, width, height, color):
        super(Brick, self).__init__()

        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.color = color

        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = pygame.draw.rect(self.surface, self.color, (0, 0, self.width, self.height))
        self.rect.update(self.left, self.top, self.width, self.height)
