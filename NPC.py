from settings import *
import pygame as pg
import math
from main import *
from BaseTank import BaseTank
import random

# Define the Player class for the player character
class NPC(BaseTank):
    def __init__(self, game, startPosition):

        #Initialialize tank properties.
        super().__init__(game, game.NPC_group, startPosition, startAngle)
        self.destination = (0,0)
        self.destinationAngle = 0
        self.add(game.NPC_group)

    def get_movement(self): #Generate movement for the NPC.
        pass

        #Rotating the tank towards that new vector

        #Increasing the tank's speed

        #Random turret movement.

    def generateDestination(self): #Generates a viable destination for the NPC.
        currentPos = self.map_pos

        if currentPos[0] > 0: #If the player is not on the top layer,
            if(self.game.map.mini_map[currentPos[0] - 1][currentPos[1]] == False): #Check if space above is empty
                pass

    # Override of the BaseTank method. So far it does nothing, but any NPC specific logic can be written here.
    def update(self):
        if self.map_pos == self.destination:
            self.generateDestination()

        self.get_movement()
        
        super().update()