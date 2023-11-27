from settings import *
import pygame as pg
from main import *
import imageio.v3 as iio



#Obstacle class for dead tanks/rubble
class DeadTank(pg.sprite.Sprite):
    def __init__(self, game, spawnPosition, rotation, image):
        super().__init__()
        self.game = game
        self.add(game.obs_group)
        self.spawnPosition = spawnPosition #input the dead NPC/Player's center attribute here
        self.image = pg.transform.rotate(image, math.degrees(rotation))
        self.rect = self.image.get_rect(center = spawnPosition)

        Explosion(self.game,self.spawnPosition).add(self.game.explosion_group)

class Explosion(pg.sprite.Sprite):
    def __init__(self, game, position):
        pg.sprite.Sprite.__init__(self)
        self.subsurfaceWidth = 180 * RESMULTX
        self.subsurfaceHeight = 180 * RESMULTY

        self.subsurfaceRect = pg.Rect(0,0, self.subsurfaceWidth, self.subsurfaceHeight)
        self.frame = 0 #There are 18 total frames

        self.image = EXPLOSIONSCALED.subsurface(self.subsurfaceRect)
        self.rect = self.image.get_rect(center = position)

    def update(self):
        frame += 1
        self.subsurfaceRect.move_ip(self.subsurfaceWidth)
        self.image = EXPLOSIONSCALED.subsurface(self.subsurfaceRect)

    