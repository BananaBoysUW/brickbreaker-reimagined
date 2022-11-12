import math


class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def copy(self):
        return Vector2D(self.x, self.y)

    def reverse_x(self):
        self.x *= -1

    def reverse_y(self):
        self.y *= -1

    def norm(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def set_angle_deg(self, theta):
        self.set_angle(math.radians(theta))

    def set_angle(self, theta):
        x = self.norm() * math.cos(theta)
        y = self.norm() * math.sin(theta)
        self.x = x
        self.y = y

    # TODO
    def set_norm(self):
        pass
