from settings import *
import pygame as pg
import math
from main import *
from BaseTank import BaseTank
import random
import imageio.v3 as iio #ignore this



# Define the NPC class for the for nonplable tanks
class NPC(BaseTank):
    def __init__(self, game, startPosition, startAngle):

        #Initialialize tank properties.
        super().__init__(game, game.player_group, startPosition, startAngle)
        self.add(game.NPC_group)

    def get_movement(self): #Generate movement for the NPC. So far, it does nothing.
        pass

    # Override of the BaseTank method. So far it does nothing, but any NPC specific logic can be written here.
    def update(self):
        self.get_movement()
        
        super().update()
        