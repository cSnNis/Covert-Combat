from settings import *
import pygame as pg
import math
from main import *
from BaseTank import BaseTank
import random

forwardState = 1
decelerationState = 2
backwardState = 3
possibleStates = [forwardState, forwardState, decelerationState, backwardState]

# Define the NPC class for the for nonplable tanks
class NPC(BaseTank):
    def __init__(self, game, startPosition):

        #Initialialize tank properties.
        super().__init__(game, game.NPC_group, startPosition)

        #Pathfinding variables
        self.direction = 0 #The direction the NPC is currently aiming to go. It is picked by self.generateDirection
        self.turret_direction = 0 #The direction the turret is tending towards.

        self.ShouldRotate = True
        self.RotatePositive = False #Randomly set by generateDirection()
        self.movementState = decelerationState
        self.changeDirection()

        self.engine_sound = pg.mixer.Sound(engine_sound_path)
        self.wall_thud_sound = WALLTHUD
        self.wall_thud_sound.set_volume(wall_thud_volume)

        self.add(game.NPC_group)

    def get_movement(self): #Generate movement for the NPC, given it's angle, intended direction, and current state.
        #Rotating the tank towards self.direction.
        if self.ShouldRotate:
            if abs(self.angle - self.direction) > 1:
                if self.RotatePositive: #Randomly set inside changeDirection. "Positive" means counterclockwise.
                    if self.angle > self.direction:
                        self.angle += player_rot_speed * self.game.delta_time
                    else:
                        self.angle -= player_rot_speed * self.game.delta_time
                else:
                    if self.angle > self.direction:
                        self.angle -= player_rot_speed * self.game.delta_time
                    else:
                        self.angle += player_rot_speed * self.game.delta_time

        #Apply acceleration, depending on the current state.
        match self.movementState:
            case 1:# forward state
                self.ShouldRotate = True
                self.stopped = False
                self.speed += player_accel * self.game.delta_time
                self.engine_sound.set_volume(self.speed/5)
                if self.engine_sound.get_num_channels() == 0:
                    pg.mixer.Channel(4).play(self.engine_sound)
            case 2: # Deceleration state. This is defaulted to when the NPC collides with something.
                self.speed *= 1 - (player_deceleration * self.game.delta_time)

                if abs(self.speed) < accelsens or self.deflectionSpeed < accelsens: #Once fully decelerated, change states.
                    self.speed = 0
                    self.stopped = True
                    self.ShouldRotate = True #Begin having the tank rotate again. This is switched off whenever there is a collision.
                    self.engine_sound.stop()
                    self.changeDirection()
                    self.changeMovementState()
                    self.engine_sound.stop()
            case 3: #backward state
                self.ShouldRotate = True
                self.stopped = False
                self.speed -= player_accel * self.game.delta_time
                self.engine_sound.set_volume(self.speed/5)
                if self.engine_sound.get_num_channels() == 0:
                    pg.mixer.Channel(4).play(self.engine_sound)
        
        self.engine_sound.set_volume(self.speed/5)

        #Random turret movement.
        if abs(self.turret_angle - self.turret_direction) > 1:
                if self.RotatePositive: #Randomly set inside changeDirection. "Positive" means counterclockwise.
                    self.turret_angle += player_rot_speed * self.game.delta_time
                else:
                    self.turret_angle -= player_rot_speed * self.game.delta_time

    def changeDirection(self): #Generates a viable destination for the NPC.
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
                    possibleDestinations.append(.75 * math.pi)
                if self.game.map.mini_map[indexY - 1][indexX] == False: #Above; 2
                    possibleDestinations.append(math.pi / 2)
                if not AtRightEdge and self.game.map.mini_map[indexY - 1][indexX + 1] == False: #Top right; 3
                    possibleDestinations.append(math.pi / 4)
            if (indexY < mapHeight): #Checking the cells adjacent and to the bottom
                if not AtLeftEdge and self.game.map.mini_map[indexY + 1][indexX - 1] == False: #Bottom left; 7
                    possibleDestinations.append(1.25 * math.pi)
                if self.game.map.mini_map[indexY + 1][indexX] == False: #Below; 8
                    possibleDestinations.append(1.5 * math.pi)
                if not AtRightEdge and self.game.map.mini_map[indexY + 1][indexX + 1] == False: #Bottom right; 9
                    possibleDestinations.append(1.75 * math.pi)
        
                #Checking cells to the left and right
            if not AtLeftEdge and self.game.map.mini_map[indexY][indexX - 1] == False: #Left
                possibleDestinations.append(math.pi)
            if not AtRightEdge and self.game.map.mini_map[indexY][indexX + 1] == False: #Bottom right
                possibleDestinations.append(0)

            self.direction = random.choice(possibleDestinations) + random.uniform((-math.pi/8), (math.pi/8)) % math.tau
            self.turret_direction = random.uniform(0, math.tau)
            self.RotatePositive = random.choice((True, False)) 
        except(IndexError):
            print('My game-breaking position was ',x, y)

    def changeMovementState(self):
        self.movementState = random.choice(possibleStates)

    # Override of the BaseTank method. So far it does nothing, but any NPC specific logic can be written here.
    def update(self):
        super().update()

        if self.movementState != decelerationState: #If it is moving;

            if self.isColliding[0]: #If the NPC has collided with something other than an NPC this frame, then begin decelerating and set a new course
                self.ShouldRotate = False
                self.movementState = decelerationState
                self.direction = self.deflectionAngle
            
            else: #If there have been no collisions this frame, 
                if random.random() < .01: #Then there is a 1 in 100 chance per frame to change direction
                    self.changeDirection()
                elif random.random() < .05: #If it hasn't collided or changed direciton, then there is a 1 in 20 chance for it to change movement state.
                    self.changeMovementState()

        self.get_movement()
        