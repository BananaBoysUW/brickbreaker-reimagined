import pygame
from pygame.locals import (QUIT, KEYDOWN, K_ESCAPE)

from Paddle import Paddle
from Ball import Ball
from Bricks import Bricks
from KeyboardController import KeyboardController
from SerialGloveController import SerialGloveController


BLACK = 0, 0, 0
WHITE = 255, 255, 255


class Game:
    def __init__(self):
        pygame.init()

        # self.screen_dimensions = self.width, self.height = pygame.display.Info().current_w, pygame.display.Info().current_h - 100
        self.screen_dimensions = self.width, self.height = 800, 1000
        self.color = BLACK
        self.screen = pygame.display.set_mode(self.screen_dimensions)
        self.fps = 30
        self.time_step = 1.0 / self.fps
        self.PPM = 1.0

        self.paddle = Paddle(width=60, height=15, color=WHITE, *self.screen_dimensions)
        self.ball = Ball(diameter=10, color=WHITE, speed=15, starting_pos_ratio=3/4, *self.screen_dimensions)
        self.ball1 = Ball(diameter=50, color=(150, 150, 150), speed=15, starting_pos_ratio=3/4, *self.screen_dimensions)
        self.bricks = Bricks(bg_color=self.color, starting_pos_ratio=3/4, *self.screen_dimensions)

        self.controller = self.select_controller()

        self.clock = pygame.time.Clock()

    def select_controller(self):
        controller = SerialGloveController()
        if controller.is_active():
            return controller

        return KeyboardController(2)

    def check_collisions(self):
        for ball in [self.ball, self.ball1]:
            if ball.rect.clipline(self.paddle.rect.topleft, self.paddle.rect.topright) or ball.rect.top <= 0:
                ball.velocity.reverse_y()

            if ball.rect.right >= ball.max_pos.x or ball.rect.left <= 0:
                ball.velocity.reverse_x()

            if ball.rect.bottom > ball.max_pos.y:
                ball.lose()

            for brick in self.bricks.brick_list:
                remove = False
                if ball.rect.clipline(brick.rect.topleft, brick.rect.bottomleft) or ball.rect.clipline(brick.rect.topright, brick.rect.bottomright):
                    ball.velocity.reverse_x()
                    remove = True
                if ball.rect.clipline(brick.rect.topleft, brick.rect.topright) or ball.rect.clipline(brick.rect.bottomleft, brick.rect.bottomright):
                    ball.velocity.reverse_y()
                    remove = True

                if remove:
                    self.bricks.remove_brick(brick)

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

            self.clock.tick(self.fps)


if __name__ == "__main__":
    Game().run()
