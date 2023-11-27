from settings import *
import pygame as pg
from main import *



#Obstacle class for dead tanks/rubble
class DeadTank(pg.sprite.Sprite):
    def __init__(self, game, spawnPosition, rotation, image):
        super().__init__()
        self.game = game
        self.add(game.obs_group)
        self.spawnPosition = spawnPosition #input the dead NPC/Player's center attribute here
        '''We will most likely need to add a new input for which image path to choose 
        (for when there's different colors), for now GD is the default'''
        self.image = pg.transform.rotate(image, math.degrees(rotation))
        self.rect = self.image.get_rect(center = spawnPosition)

        self.explosion_sound = TANKEXPLOSION
        self.explosion_sound.set_volume(tank_death_volume)
        pg.mixer.Channel(5).play(self.explosion_sound)
        