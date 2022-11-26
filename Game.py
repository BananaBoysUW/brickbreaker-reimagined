import pygame
from pygame.locals import (QUIT, KEYDOWN, K_ESCAPE)

import json

from Paddle import Paddle
from Ball import Ball
from Brick import Brick
from KeyboardController import KeyboardController
from SerialGloveController import SerialGloveController


BLACK = 0, 0, 0
WHITE = 255, 255, 255


class Game:
    def __init__(self):
        pygame.init()

        # self.screen_dimensions = self.width, self.height = pygame.display.Info().current_w, pygame.display.Info().current_h - 100
        self.screen_dimensions = self.width, self.height = 800, 800
        self.color = BLACK
        self.screen = pygame.display.set_mode(self.screen_dimensions)
        self.fps = 30
        self.time_step = 1.0 / self.fps
        self.PPM = 1.0

        self.paddle = Paddle(width=60, height=15, color=WHITE, *self.screen_dimensions)
        self.ball = Ball(diameter=10, color=WHITE, speed=15, *self.screen_dimensions)
        self.ball1 = Ball(diameter=50, color=(150, 150, 150), speed=15, *self.screen_dimensions)
        self.bricks = self.get_bricks()

        self.controller = self.select_controller()

        self.clock = pygame.time.Clock()

    def get_bricks(self):
        with open("rects.json", "r") as f:
            rects = json.load(f)
            rects = self.scale(rects)
            bricks = [Brick(*rect[0], color=rect[1]) for rect in rects]

            return bricks

    def scale(self, rects):
        # TODO: make scaling take into account height
        max_x = 0
        max_y = 0

        for rect in rects:
            max_x = max(max_x, max(rect[0][0], rect[0][2]))
            max_y = max(max_y, max(rect[0][1], rect[0][3]))

        scale_factor = self.width / max_x

        rects = [([i * scale_factor for i in r[0]], r[1]) for r in rects]

        return rects

    def select_controller(self):
        controller = SerialGloveController()
        if controller.is_active():
            return controller

        return KeyboardController(2)

    def render(self):
        self.screen.fill(self.color)

        for brick in self.bricks:
            self.screen.blit(brick.surface, brick.rect)

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
            self.ball1.update(self.paddle)
            self.ball.update(self.paddle)

            self.render()

            self.clock.tick(self.fps)


if __name__ == "__main__":
    Game().run()
