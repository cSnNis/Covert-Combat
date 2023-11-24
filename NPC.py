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

# Define the Player class for the player character
class NPC(BaseTank):
    def __init__(self, game, startPosition):

        #Initialialize tank properties.
        super().__init__(game, game.NPC_group, startPosition)

        #Pathfinding variables
        self.direction = 0 #The direction the NPC is currently aiming to go. It is picked by self.generateDirection
        self.turret_direction = 0 #The direction the turret is tending towards.
        self.decelerateFromCollision = False
        self.RotatePositive = False #Randomly set by generateDirection()
        self.movementState = 1
        self.changeDirection()

        self.add(game.NPC_group)

    def get_movement(self): #Generate movement for the NPC, given it's angle, intended direction, and current state.
        #Rotating the tank towards self.direction.
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
                self.stopped = False
                self.speed += player_accel * self.game.delta_time
                self.engine_sound.set_volume(self.speed/5)
                if self.engine_sound.get_num_channels() == 0:
                    self.engine_sound.play(-1)
            case 2: # Deceleration state. This is defaulted to when the NPC collides with something.
                self.speed *= 1 - (player_deceleration * self.game.delta_time)

                if abs(self.speed) < accelsens: #Once fully decelerated, change states.
                    self.stopped = True
                    self.engine_sound.stop()
                    self.deflectionSpeed = 0

                    if self.speed > 0: #If the NPC was moving forward before decelerating,
                        self.movementState = backwardState #The NPC should reverse
                    else:
                        self.movementState = forwardState
                    
                    self.changeDirection() #and also get a new direction
                    self.engine_sound.stop()
            case 3: #backward state
                self.stopped = False
                self.speed -= player_accel * self.game.delta_time
                self.engine_sound.set_volume(self.speed/5)
                if self.engine_sound.get_num_channels() == 0:
                    self.engine_sound.play(-1)
        
        self.engine_sound.set_volume(self.speed/5)

        #Random turret movement.

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

    def changeMovementState(self):
        self.movementState = random.choice(possibleStates)

    # Override of the BaseTank method. So far it does nothing, but any NPC specific logic can be written here.
    def update(self):
        if self.isColliding[0]: #If there was a collision this frame, then begin decelerating and set a new course
            pg.draw.rect(self.game.screen, 'green', self.rect)
            self.movementState = decelerationState
            self.direction = self.deflectionAngle
            self.RotatePositive = random.choice((True, False)) #Also, flip which way the NPC tank is rotating, because why not.
        elif random.random() < .05: #If the NPC is not colliding, then there is a 1 in 20 chance per frame to change direction
            #self.changeDirection()
            pass
        elif random.random() < .1: #If it hasn't collided or changed direciton, then there is a 1 in 10 chance for it to change movement state.
            self.changeMovementState()

        pg.draw.line(self.game.screen, 'green', (self.xDisplay, self.yDisplay), (self.xDisplay + math.cos(self.direction) * COORDINATEMULTX, self.yDisplay + math.sin(-self.direction) * COORDINATEMULTY), 2)

        self.get_movement()
        
        super().update()