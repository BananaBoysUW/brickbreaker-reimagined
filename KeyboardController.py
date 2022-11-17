import pygame


class KeyboardController:
    def __init__(self, velocity):
        self.initial_x = 50
        self.velocity = velocity

        self.x = self.initial_x

    def reset(self):
        self.x = self.initial_x

    def move_right(self):
        self.x = min(self.x + self.velocity, 100)

    def move_left(self):
        self.x = max(self.x - self.velocity, 0)

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.move_right()
        if keys[pygame.K_LEFT]:
            self.move_left()

    def get_x(self):
        """range: [0, 100]"""
        self.update()
        return self.x
