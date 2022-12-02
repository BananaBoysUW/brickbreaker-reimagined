import pygame
import json

from Brick import Brick
from MapMode import MapMode
import QuadTree
import ShapeDetection

# Number of blocks for geohash
BLOCKS_X = 8
BLOCKS_Y = 8


class Bricks(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, starting_pos_ratio, bg_color, mode, image_path):
        super(Bricks, self).__init__()
        self.width = screen_width
        self.height = screen_height * starting_pos_ratio
        self.bg_color = bg_color

        self.brick_list = self.get_bricks(mode, image_path)
        self.zones = self.get_zones()
        self.geohash = self.get_geohash()

        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.surface.get_rect()

        self.render()

    def get_bricks(self, mode, image_path):
        rects = None

        if mode == MapMode.QUADTREE:
            rects = QuadTree.convert(image_path)

        if mode == MapMode.OPENCV:
            rects = ShapeDetection.convert(image_path)

        return [Brick(*rect) for rect in rects]

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

    def get_relevant_bricks(self, ball):
        zones = self.get_ball_zones(ball)
        return list(set([brick for zone in zones for brick in self.geohash[zone]]))
