import pygame
import random
from Vector2D import Vector2D


class Ball(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, diameter, color, speed, starting_pos_ratio):
        super(Ball, self).__init__()

        self.diameter = diameter
        self.radius = self.diameter / 2
        self.color = color

        self.initial_pos = Vector2D(screen_width / 2, screen_height * starting_pos_ratio)
        self.pos = self.initial_pos.copy()
        self.velocity = Vector2D(speed, 0)
        self.max_pos = Vector2D(screen_width, screen_height)

        self.surface = pygame.Surface((self.diameter, self.diameter), pygame.SRCALPHA)
        self.rect = pygame.draw.circle(self.surface, self.color, (self.radius, self.radius), self.radius)

        self.reset_pos()

    def update_pos(self):
        self.rect.update(self.pos.x, self.pos.y, self.diameter, self.diameter)

    def reset_pos(self):
        self.pos = self.initial_pos.copy()
        self.update_pos()
        self.velocity.set_angle_deg(random.randrange(45, 135))

    def lose(self):
        self.reset_pos()

    def update(self):
        self.pos += self.velocity
        self.update_pos()

    def center(self):
        return self.pos + Vector2D(self.radius, self.radius)

    def reflect(self, reflection_axis):
        self.velocity = self.velocity - 2 * self.velocity.proj(reflection_axis)

    def check_collisions(self, paddle, bricks):
        if self.rect.clipline(paddle.rect.topleft, paddle.rect.topright):
            self.velocity.y = -1 * abs(self.velocity.y)

        if self.rect.top <= 0:
            self.velocity.y = abs(self.velocity.y)

        if self.rect.right >= self.max_pos.x:
            self.velocity.x = -1 * abs(self.velocity.x)

        if self.rect.left <= 0:
            self.velocity.x = abs(self.velocity.x)

        if self.rect.bottom > self.max_pos.y:
            self.lose()

        for brick in bricks.get_relevant_bricks(self):
            collision_axis = brick.collide_detect_ball(self)
            if collision_axis:
                self.reflect(collision_axis)
                bricks.remove_brick(brick)
