import pygame as pg
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
  def __init__(self, x, y):
      super().__init__()
      self.image = pg.Surface((100, 100), pg.SRCALPHA)
      self.image.fill((100, 100, 100, 0))
      self.rect = self.image.get_rect()
      self.rect.topleft = (x * 100, y * 100)
      self.mask = pg.mask.from_surface(self.image)
class Map:
    def __init__(self, game):
        self.game = game
        self.mini_map = mini_map
        self.world_map = {}
        self.walls = pg.sprite.Group()
        self.get_map()
        self.tile_image = pg.image.load('download (6).jpg').convert_alpha()
    def get_map(self):
        for j, row in enumerate(self.mini_map):
            for i, value in enumerate(row):
                if value:
                    self.world_map[(i,j)] = value
                    if value == 1:
                        wall = Wall(i, j)  # Create a wall sprite
                        self.walls.add(wall)  # Add the wall sprite to the group
    def draw(self):
        for pos in self.world_map:
            x = pos[0] * 100
            y = pos[1] * 100
            self.game.screen.blit(self.tile_image, (x, y))
        self.walls.draw(self.game.screen)  # Draw the wall sprites
  