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
        super().__init__(game, game.NPC_group, startPosition)
        self.destination = (0,0)
        self.destinationAngle = 0
        self.decelerateFromCollision = False
        self.generateDestination()

        self.add(game.NPC_group)

    def get_movement(self): #Generate movement for the NPC.
        pass

        #Rotating the tank towards that new vector

        #Accelerating the NPC, or decelerating otherwise.

        #Random turret movement.

    def generateDestination(self): #Generates a viable destination for the NPC.
        x, y = self.map_pos
        indexX, indexY = self.map_pos[0] - 1, self.map_pos[1] - 1 #Refer to map.py for why there is an index coordinate and actual coordinate.
        mini_map = self.game.map.mini_map
        mapWidth = len(mini_map[0]) - 1
        mapHeight = len(mini_map) - 1
        AtLeftEdge = (indexX == 0)
        AtRightEdge = (indexX == mapWidth)

        possibleDestinations = []

        #Check which of the adjacent cells are empty.
        if (y > 0): #Checking the cells adjacent and to the top.
            if not AtLeftEdge and self.game.map.mini_map[indexY - 1][indexX - 1] == False: #Top left
                possibleDestinations.append((x - 1, y - 1))
            if self.game.map.mini_map[indexY - 1][indexX] == False: #Above
                possibleDestinations.append((x, y - 1))
            if not AtRightEdge and self.game.map.mini_map[indexY - 1][indexX + 1] == False: #Top right
                possibleDestinations.append((x + 1, y - 1))
        if (y < mapHeight): #Checking the cells adjacent and to the bottom
            if not AtLeftEdge and self.game.map.mini_map[indexY + 1][indexX - 1] == False: #Bottom left
                possibleDestinations.append((x - 1, y + 1))
            if self.game.map.mini_map[indexY + 1][indexX] == False: #Below
                possibleDestinations.append((x, y + 1))
            if not AtRightEdge and self.game.map.mini_map[indexY + 1][indexX + 1] == False: #Bottom right
                possibleDestinations.append((x + 1, y + 1))
    
            #Checking cells to the left and right
        if not AtLeftEdge and self.game.map.mini_map[indexY][indexX - 1] == False: #Left
            possibleDestinations.append((x - 1, y))
        if not AtRightEdge and self.game.map.mini_map[indexY][indexX + 1] == False: #Bottom right
            possibleDestinations.append((x + 1, y))

        for location in possibleDestinations:
            pg.draw.rect(self.game.screen, 'green', pg.Rect(location[0] * COORDINATEMULTX, location[1] * COORDINATEMULTY, 100, 100))
        
        return random.choice(possibleDestinations)

    # Override of the BaseTank method. So far it does nothing, but any NPC specific logic can be written here.
    def update(self):
        self.generateDestination()
        if self.map_pos == self.destination:
            self.generateDestination()
        if self.isColliding[0]: #If there was a collision this frame, then begin decelerating and set a new course
            self.generateDestination()
            self.decelerateFromCollision = True

        self.get_movement()
        
        super().update()