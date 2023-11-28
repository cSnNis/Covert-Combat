
import pygame as pg
from settings import *

_ = False 
mini_map = [ #On screen, the top right space is (1,1), whereas when indexing this list, the top right space is (0,0) where element 1 is the row number, and element 2 is the cell number of that row
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,_,_,_,_,_,_,_,_,_,_,_,_,_,_,1],
    [1,_,_,_,_,_,_,_,_,_,_,1,_,_,_,1],
    [1,_,_,_,_,_,_,1,1,_,_,1,_,_,_,1],
    [1,1,1,1,_,_,_,1,_,_,_,_,_,_,_,1],
    [1,_,_,_,_,_,_,_,_,_,_,_,1,_,_,1],
    [1,_,_,_,_,_,_,_,_,_,_,_,1,_,_,1],
    [1,_,_,_,1,_,_,_,_,_,_,_,_,_,_,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

class Wall(pg.sprite.Sprite):
    def __init__(self, x, y, image_path, dimensions):
        super().__init__()
        self.image = pg.image.load(image_path).convert_alpha(); self.image = pg.transform.scale(self.image, (dimensions[0] * RESMULTX, dimensions[1] * RESMULTY))
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
        obstacle_mapping = {
            2: 'images/obstacles/0001.png',
            3: 'images/obstacles/0002.png',
            4: 'images/obstacles/0003.png',
            5: 'images/obstacles/0004.png',
            6: 'images/obstacles/0005.png',
            7: 'images/obstacles/0006.png',
            8: 'images/obstacles/0007.png',
            9: 'images/obstacles/0008.png',
            10: 'images/obstacles/0009.png',
            11: 'images/obstacles/0010.png',
            12: 'images/obstacles/0011.png',
            13: 'images/obstacles/0012.png',
            14: 'images/obstacles/0013.png',
            15: 'images/obstacles/0014.png',
            16: 'images/obstacles/0015.png',
            17: 'images/obstacles/0016.png',
            18: 'images/obstacles/0017.png',
            19: 'images/obstacles/0018.png',
            20: 'images/obstacles/0019.png',
            21: 'images/obstacles/0020.png',
            22: 'images/obstacles/0021.png',
            23: 'images/obstacles/0022.png',
            24: 'images/obstacles/0023.png',
            25: 'images/obstacles/0024.png',
            26: 'images/obstacles/0025.png',
            27: 'images/obstacles/0026.png',
        }

        for j, row in enumerate(self.mini_map):
            for i, value in enumerate(row):
                if value:
                    self.world_map[(i, j)] = value
                    if value == 1:
                        wall = Wall(i, j, tile_sprite_path, (100, 100))
                        self.walls.add(wall)
                    elif value == 10:
                        obstacle = Wall(i, j, obstacle_mapping[value], (1000, 100))
                        self.walls.add(obstacle)

    def draw(self):
        self.walls.draw(self.game.screen)
        self.game.obs_group.draw(self.game.screen)
  