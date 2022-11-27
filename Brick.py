import pygame
import numpy as np

from Vector2D import Vector2D


class Brick(pygame.sprite.Sprite):
    def __init__(self, points, color):
        super(Brick, self).__init__()

        self.points = points
        self.color = color

        self.zone_numbers = []

        self.point_pairs = lambda: zip(self.points, self.points[1:] + self.points[:1])

        left, top, width, height = self.get_rect_vals()

        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = pygame.draw.polygon(self.image, self.color, [(x - left, y - top) for x, y in self.points])
        self.rect.update(left, top, width, height)

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

    def reflect_ball(self, ball, reflection_axis):
        ball.velocity = ball.velocity - 2 * ball.velocity.proj(reflection_axis)

    def collide_detect_ball(self, ball):
        for p1, p2 in self.point_pairs():
            a = Vector2D(*p1)
            b = Vector2D(*p2)
            c = ball.center()

            ab = b - a
            ac = c - a
            bc = c - b
            ba = a - b

            if ac.angle_with_deg(ab) < 90 and bc.angle_with_deg(ba) < 90:
                perp = ac.perp(ab)
                if perp.norm() <= ball.radius:
                    print("collision!")
                    self.reflect_ball(ball, perp)
                    return True

            if ac.norm() <= ball.radius:
                self.reflect_ball(ball, ac)
                return True

            if bc.norm() <= ball.radius:
                self.reflect_ball(ball, bc)
                return True

        return False
