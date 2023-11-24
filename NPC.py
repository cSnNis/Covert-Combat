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
        self.direction = 0 #The direction the NPC is currently aiming to go. It is picked by self.generateDirection
        self.decelerateFromCollision = False
        self.RotatePositive = False #Randomly set by generateDirection()
        self.generateDirection()

        print("My start position was",startPosition)

        self.add(game.NPC_group)

    def get_movement(self): #Generate movement for the NPC.
        #Rotating the tank towards self.destination_real point.
        if self.RotatePositive:
            if self.angle > self.direction:
                self.angle += player_rot_speed * self.game.delta_time
        else:
            if self.angle > self.direction:
                self.angle -= player_rot_speed * self.game.delta_time
        

        #Accelerating the NPC, or decelerating otherwise.
        if not self.decelerateFromCollision: #Accelerating forward, as normal
            self.stopped = False
            self.speed += player_accel * self.game.delta_time
            self.engine_sound.set_volume(self.speed/5)
            if self.engine_sound.get_num_channels() == 0:
                self.engine_sound.play(-1)
        else: #We must've hit something, decelerate.
            self.speed *= 1 - (player_deceleration * self.game.delta_time)
            self.engine_sound.set_volume(abs(self.speed)/5)

            if abs(self.speed) < accelsens:
                self.stopped = True
                self.decelerateFromCollision = False #Begin moving forward again.
                self.engine_sound.stop()
                self.deflectionSpeed = 0

        #Random turret movement.

    def generateDirection(self): #Generates a viable destination for the NPC.
        x, y = self.map_pos
        indexX, indexY = self.map_pos[0] - 1, self.map_pos[1] - 1 #Refer to map.py for why there is an index coordinate and actual coordinate.
        mini_map = self.game.map.mini_map
        mapWidth = len(mini_map[0]) - 1
        mapHeight = len(mini_map) - 1
        AtLeftEdge = (indexX == 0)
        AtRightEdge = (indexX == mapWidth)

        possibleDestinations = []

        #Check which of the adjacent cells are empty.
        try:
            if (indexY > 0): #Checking the cells adjacent and to the top.

                #Which direction is represented by a number, corresponding to an imaginary tic-tac-toe board number 1-9 surrounding the NPC, which starts at the top left corner. 6 represents the NPC.

                if not AtLeftEdge and self.game.map.mini_map[indexY - 1][indexX - 1] == False: #Top left; 1
                    #possibleDestinations.append((x - 1, y - 1))
                    possibleDestinations.append(.75 * math.pi)
                if self.game.map.mini_map[indexY - 1][indexX] == False: #Above; 2
                    #possibleDestinations.append((x, y - 1))
                    possibleDestinations.append(math.pi / 2)
                if not AtRightEdge and self.game.map.mini_map[indexY - 1][indexX + 1] == False: #Top right; 3
                    #possibleDestinations.append((x + 1, y - 1))
                    possibleDestinations.append(math.pi / 4)
            if (indexY < mapHeight): #Checking the cells adjacent and to the bottom
                if not AtLeftEdge and self.game.map.mini_map[indexY + 1][indexX - 1] == False: #Bottom left; 7
                    #possibleDestinations.append((x - 1, y + 1))
                    possibleDestinations.append(1.25 * math.pi)
                if self.game.map.mini_map[indexY + 1][indexX] == False: #Below; 8
                    #possibleDestinations.append((x, y + 1))
                    possibleDestinations.append(1.5 * math.pi)
                if not AtRightEdge and self.game.map.mini_map[indexY + 1][indexX + 1] == False: #Bottom right; 9
                    #possibleDestinations.append((x + 1, y + 1))
                    possibleDestinations.append(1.75 * math.pi)
        
                #Checking cells to the left and right
            if not AtLeftEdge and self.game.map.mini_map[indexY][indexX - 1] == False: #Left
                #possibleDestinations.append((x - 1, y))
                possibleDestinations.append(math.pi)
            if not AtRightEdge and self.game.map.mini_map[indexY][indexX + 1] == False: #Bottom right
                #possibleDestinations.append((x + 1, y))
                possibleDestinations.append(0)

            self.direction = random.choice(possibleDestinations) + random.uniform((-math.pi/8), (math.pi/8)) % math.tau
            self.RotatePositive = random.choice((True, False)) 
        except(IndexError):
            print('My game-breaking position was ',x, y)

    # Override of the BaseTank method. So far it does nothing, but any NPC specific logic can be written here.
    def update(self):
        if self.isColliding[0]: #If there was a collision this frame, then begin decelerating and set a new course
            pg.draw.rect(self.game.screen, 'green', self.rect)
            #self.generateDirection()
            self.direction = (self.direction + math.pi) % math.tau
            self.decelerateFromCollision = True
        elif random.random() < .01 : #Otherwise, 1 in 100 chance per frame of changing direction.
            self.generateDirection()


        self.get_movement()
        
        super().update()