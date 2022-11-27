import pygame
import json

from Brick import Brick

# Number of blocks for geohash
BLOCKS_X = 8
BLOCKS_Y = 8


class Bricks(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, starting_pos_ratio, bg_color):
        super(Bricks, self).__init__()
        self.width = screen_width
        self.height = screen_height * starting_pos_ratio
        self.bg_color = bg_color

        self.brick_list = self.get_bricks()
        self.zones = self.get_zones()
        self.geohash = self.get_geohash()

        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.surface.get_rect()

        self.render()

    def ltrb_rect_to_points(self, rects):
        rects_as_points = []
        for rect in rects:
            (l, t, r, b), color = rect
            rects_as_points.append((((l, t), (r, t), (r, b), (l, b)), color))

        return rects_as_points

    def get_bricks(self):
        with open("rects.json", "r") as f:
            rects = json.load(f)
            rects = self.ltrb_rect_to_points(rects)
            brick_list = [Brick(rect[0], color=rect[1]) for rect in rects]

            return brick_list

    def get_zones(self):
        zone_width = self.width / BLOCKS_X
        zone_height = self.height / BLOCKS_Y

        zones = []

        for i in range(BLOCKS_X):
            for j in range(BLOCKS_Y):
                zones.append(pygame.Rect(i * zone_width, j * zone_height, zone_width, zone_height))

        return zones

    def get_geohash(self):
        geohash = []
        for i, zone in enumerate(self.zones):
            bricks_in_zone = []
            for brick in self.brick_list:
                if zone.colliderect(brick.rect):
                    brick.add_zone_number(i)
                    bricks_in_zone.append(brick)
            geohash.append(bricks_in_zone)
        return geohash

    def render(self):
        self.surface.fill(self.bg_color)

        for brick in self.brick_list:
            self.surface.blit(brick.image, brick.rect)

    def remove_brick(self, brick):
        for i in brick.zone_numbers:
            self.geohash[i].remove(brick)

        self.brick_list.remove(brick)

    def update(self):
        self.render()

    def get_ball_zones(self, ball):
        return [i for i, zone in enumerate(self.zones) if zone.colliderect(ball.rect)]

    def get_relevant_bricks(self, ball) -> set:
        zones = self.get_ball_zones(ball)
        return list(set([brick for zone in zones for brick in self.geohash[zone]]))
