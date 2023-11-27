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

    def load_animation(self):
        frames = []