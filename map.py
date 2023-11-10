import pygame as pg
from settings import *

_ = False 
mini_map = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,_,_,_,_,_,_,_,_,_,_,_,_,_,_,1],
    [1,_,_,_,_,_,_,_,_,_,_,_,_,_,_,1],
    [1,_,_,_,_,_,1,_,_,_,_,_,_,_,_,1],
    [1,_,_,_,_,_,1,_,_,_,_,1,1,1,1,1],
    [1,_,_,_,_,1,1,_,_,_,_,1,_,_,_,1],
    [1,_,_,_,_,_,_,_,_,_,_,_,_,_,_,1],
    [1,_,_,_,_,1,_,_,_,_,_,1,_,_,_,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

class Wall(pg.sprite.Sprite):
  def __init__(self, x, y, image):
      super().__init__()
      self.image = image
      self.rect = self.image.get_rect()
      self.rect.topleft = (x * COORDINATEMULTX, y * COORDINATEMULTY)
      self.mask = pg.mask.from_surface(self.image)

class Map:
    def __init__(self, game):
        self.game = game
        self.mini_map = mini_map
        self.world_map = {}
        self.walls = pg.sprite.Group()
        self.tile_image = pg.transform.scale(pg.image.load(tile_sprite_path).convert_alpha(), COORDINATEMULT) 
        self.get_map() 
   
    def get_map(self): #From the mini_map, create a 
        for j, row in enumerate(self.mini_map):
            for i, value in enumerate(row):
                if value:
                    self.world_map[(i,j)] = value
                    if value == 1:
                        wall = Wall(i, j, self.tile_image)  # Create a wall sprite
                        self.walls.add(wall)  # Add the wall sprite to the group
    
    def draw(self):
        # for pos in self.world_map:
        #     x = pos[0] * 100
        #     y = pos[1] * 100
        #     self.game.screen.blit(self.tile_image, (x, y))
        self.walls.draw(self.game.screen)  # Draw the wall sprites
  