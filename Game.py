import pygame
from pygame.locals import (QUIT, KEYDOWN, K_ESCAPE)

from Paddle import Paddle
from Ball import Ball
from Bricks import Bricks
from KeyboardController import KeyboardController
from SerialGloveController import SerialGloveController


BLACK = 0, 0, 0
WHITE = 255, 255, 255

WIDTH = 800
HEIGHT = 1000

FPS = 90
STARTING_POS_RATIO = 3/4
OFFSET_ANGLE = 25


class Game:
    def __init__(self, mode, image_path):
        pygame.init()

        # self.screen_dimensions = self.width, self.height = pygame.display.Info().current_w, pygame.display.Info().current_h - 100
        self.screen_dimensions = self.width, self.height = WIDTH, HEIGHT
        self.color = BLACK
        self.screen = pygame.display.set_mode(self.screen_dimensions)
        self.time_step = 1.0 / FPS
        self.PPM = 1.0

        self.paddle = Paddle(width=80, height=15, color=WHITE, *self.screen_dimensions)
        self.ball = Ball(diameter=10, color=WHITE, speed=5, starting_pos_ratio=STARTING_POS_RATIO, offset_angle=OFFSET_ANGLE, *self.screen_dimensions)
        self.ball1 = Ball(diameter=50, color=(150, 150, 150), speed=5, starting_pos_ratio=STARTING_POS_RATIO, offset_angle=OFFSET_ANGLE, *self.screen_dimensions)
        self.bricks = Bricks(bg_color=self.color, starting_pos_ratio=STARTING_POS_RATIO, mode=mode, image_path=image_path, *self.screen_dimensions)

        self.controller = self.select_controller()

        self.clock = pygame.time.Clock()

    def select_controller(self):
        controller = SerialGloveController()
        if controller.is_active():
            return controller

        return KeyboardController(1)

    def check_collisions(self):
        for ball in [self.ball, self.ball1]:
            ball.check_collisions(self.paddle, self.bricks)

    def render(self):
        self.screen.fill(self.color)

        self.screen.blit(self.bricks.surface, self.bricks.rect)
        self.screen.blit(self.paddle.surface, self.paddle.rect)
        self.screen.blit(self.ball.surface, self.ball.rect)
        self.screen.blit(self.ball1.surface, self.ball1.rect)

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    running = False

            self.paddle.update(self.controller.get_x())
            self.ball1.update()
            self.ball.update()
            self.bricks.update()

            self.check_collisions()

            self.render()

            self.clock.tick(FPS)


if __name__ == "__main__":
    Game().run()
