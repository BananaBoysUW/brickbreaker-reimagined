import pygame

from Paddle import Paddle
from Ball import Ball
from KeyboardController import KeyboardController
from SerialGloveController import SerialGloveController

BLACK = 0, 0, 0
WHITE = 255, 255, 255


class Game:
    def __init__(self):
        pygame.init()

        self.screen_dimensions = self.width, self.height = pygame.display.Info().current_w, pygame.display.Info().current_h - 100
        # self.screen_dimensions = self.width, self.height = 800, 600
        self.color = BLACK
        self.screen = pygame.display.set_mode(self.screen_dimensions)
        self.fps = 30

        self.paddle = Paddle(width=60, height=15, color=WHITE, *self.screen_dimensions)
        self.ball = Ball(diameter=10, color=WHITE, speed=15, *self.screen_dimensions)
        self.ball1 = Ball(diameter=100, color=(150, 150, 150), speed=15, *self.screen_dimensions)
        self.controller = self.select_controller()

        self.clock = pygame.time.Clock()

    def select_controller(self):
        controller = SerialGloveController()
        if controller.is_active():
            return controller

        return KeyboardController(2)

    def render(self):
        self.screen.fill(self.color)
        self.screen.blit(self.paddle.surface, self.paddle.rect)
        self.screen.blit(self.ball.surface, self.ball.rect)
        self.screen.blit(self.ball1.surface, self.ball1.rect)

        pygame.display.flip()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        break
                elif event.type == pygame.QUIT:
                    break

            self.clock.tick(self.fps)

            self.paddle.update(self.controller.get_x())
            self.ball1.update(self.paddle)
            self.ball.update(self.paddle)

            self.render()


if __name__ == "__main__":
    Game().run()
