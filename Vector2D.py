import math


class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if isinstance(other, Vector2D):
            return self.x * other.x + self.y * other.y

    def __rmul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector2D(self.x * other, self.y * other)

    def copy(self):
        return Vector2D(self.x, self.y)

    def reverse_x(self):
        self.x *= -1

    def reverse_y(self):
        self.y *= -1

    def norm(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def set_angle(self, theta):
        x = self.norm() * math.cos(theta)
        y = self.norm() * math.sin(theta)
        self.x = x
        self.y = y

    def set_angle_deg(self, theta):
        self.set_angle(math.radians(theta))

    def rotate_ccw(self, theta):
        x = self.x
        y = self.y
        self.x = (math.cos(theta) * x) - (math.sin(theta) * y)
        self.y = (math.sin(theta) * x) + (math.cos(theta) * y)

    def rotate_ccw_deg(self, theta):
        self.rotate_counterclockwise(math.radians(theta))

    def angle_with(self, other):
        if self.norm() * other.norm() == 0:
            return math.inf

        return math.acos(self * other / (self.norm() * other.norm()))

    def angle_with_deg(self, other):
        return math.degrees(self.angle_with(other))

    def proj(self, other):
        if other.norm() == 0:
            return math.inf

        return ((self * other) / (other.norm() ** 2)) * other

    def perp(self, other):
        return self - self.proj(other)

    # TODO
    def set_norm(self):
        pass
