import pygame
from pygame.locals import (QUIT, KEYDOWN, K_ESCAPE)
import time

from Paddle import Paddle
from Ball import Ball
from Bricks import Bricks
from KeyboardController import KeyboardController
from SerialGloveController import SerialGloveController

JINTAO_INTERVAL_SECONDS = 0.2

BLACK = 0, 0, 0
WHITE = 255, 255, 255
GREY = 40, 40, 40

WIDTH = 800

FPS = 90
STARTING_POS_RATIO = 4/7
OFFSET_ANGLE = 25


class Game:
    def __init__(self, mode=None, image_path=None, Jintao=False):
        pygame.init()

        display_width = pygame.display.Info().current_w
        display_height = pygame.display.Info().current_h

        self.screen_dimensions = self.width, self.height = WIDTH, display_height
        self.color = BLACK
        self.Jintao = Jintao

        self.entire_screen = pygame.display.set_mode(self.screen_dimensions, pygame.FULLSCREEN)
        self.entire_screen.fill(GREY)

        self.screen = pygame.Surface((self.width, self.height))
        self.rect = self.screen.get_rect()
        self.rect.move_ip(((display_width - self.width) / 2, 0))

        self.paddle = Paddle(width=80, height=15, color=WHITE, *self.screen_dimensions)
        self.balls = []
        self.add_ball(10, WHITE, 5)
        self.bricks = Bricks(bg_color=self.color, starting_pos_ratio=STARTING_POS_RATIO, mode=mode, image_path=image_path, Jintao=Jintao, *self.screen_dimensions)

        self.controller = self.select_controller()

        self.clock = pygame.time.Clock()
        self.prevTime = time.time()

    def select_controller(self):
        controller = SerialGloveController()
        if controller.is_active():
            return controller

        return KeyboardController(1)

    def add_ball(self, diameter, color, speed):
        self.balls.append(Ball(diameter=diameter, color=color, speed=speed, starting_pos_ratio=STARTING_POS_RATIO, offset_angle=OFFSET_ANGLE, *self.screen_dimensions))

    def remove_ball(self, ball):
        self.balls.remove(ball)

    def check_collisions(self):
        for ball in self.balls:
            ball.check_collisions(self.paddle, self.bricks)

    def render(self):
        self.screen.fill(self.color)

        self.screen.blit(self.bricks.surface, self.bricks.rect)
        self.screen.blit(self.paddle.surface, self.paddle.rect)
        for ball in self.balls:
            self.screen.blit(ball.surface, ball.rect)

        self.entire_screen.blit(self.screen, self.rect)

        pygame.display.flip()

    def run(self):
        prevTime = time.time()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    running = False

            if self.Jintao:
                currentTime = time.time()
                if currentTime - prevTime > JINTAO_INTERVAL_SECONDS:
                    self.add_ball(10, WHITE, 5)
                    prevTime = currentTime

            self.paddle.update(self.controller.get_x())
            for ball in self.balls:
                ball.update()
            self.bricks.update()

            self.check_collisions()

            self.render()

            self.clock.tick(FPS)


if __name__ == "__main__":
    Game().run()
