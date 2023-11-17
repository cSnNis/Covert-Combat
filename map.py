
import pygame as pg
from settings import *

_ = False 
mini_map = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,_,_,_,_,_,_,_,_,_,_,_,_,_,_,1],
    [1,_,_,_,_,_,_,_,_,2,_,_,_,_,_,1],
    [1,_,_,_,_,_,1,_,_,_,_,_,_,_,_,1],
    [1,_,_,_,_,_,1,_,_,_,_,1,1,1,1,1],
    [1,_,_,_,_,1,1,_,_,_,_,1,_,_,_,1],
    [1,_,_,_,_,_,_,_,_,_,_,_,_,_,_,1],
    [1,_,_,_,_,1,_,_,_,_,_,1,_,_,_,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

class Wall(pg.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()
        self.image = pg.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * COORDINATEMULTX, y * COORDINATEMULTY)
        self.mask = pg.mask.from_surface(self.image)

class Map:
    def __init__(self, game):
        self.game = game
        self.mini_map = mini_map
        self.world_map = {}
        self.walls = pg.sprite.Group()
        self.get_map()

    def get_map(self):
        for j, row in enumerate(self.mini_map):
            for i, value in enumerate(row):
                if value:
                    self.world_map[(i, j)] = value
                    if value == 1:
                        wall = Wall(i, j, tile_sprite_path)
                        self.walls.add(wall)
                    elif value == 2:
                        obstacle2_image = tank_sprite_path  # Replace with the actual path
                        obstacle2 = Wall(i, j, obstacle2_image)
                        self.walls.add(obstacle2)

    def draw(self):
        self.walls.draw(self.game.screen)
  