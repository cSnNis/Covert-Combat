from settings import *
import pygame as pg
from DeadTank import DeadTank
import math
import random

# Define the Player class for the player character
class BaseTank(pg.sprite.Sprite):
    def __init__(self, game, spriteGroup, startPosition):
        # Initialize the tank's attributes
        pg.sprite.Sprite.__init__(self) #Required of all pg.sprite objects
        self.add(spriteGroup)
        self.game = game
        self.x, self.y = startPosition[0] + .5, startPosition[1] + .5  # Initial tank position
        self.angle =  random.uniform(0, 2 * math.pi) # Initial tank angle

        #Loading in sprite images.
        ImageSet = random.choice(TANKSPRITELIST)

        self.xDisplay, self.yDisplay = (self.pos[0] * COORDINATEMULT[0], self.pos[1] * COORDINATEMULT[1])
        self.image = ImageSet[0]
        self.rect = self.image.get_rect()  # Create a rect for the player sprite
        self.rect.center = (self.x * COORDINATEMULTX, self.y * COORDINATEMULTY)  # Set the initial position
        
        self.turret_angle = random.uniform(0, 2 * math.pi)  # Initial turret angle
        self.turret_image = ImageSet[1]

        #Creating collision Variables
        self.collidables = [self.game.map.walls, game.player_group, game.NPC_group, game.obs_group] #Anything that should be collided with should be in this group.
        self.mask = pg.mask.from_surface(self.image) # We are only doing collisions for the body of the tank.
        self.isColliding = (False, 0) #(Is There a Collision, Reference to Object of collision.)
        self.deflectionSpeed = 0

        #Creating movement variables
        self.speed = 0
        self.stopped = True

        #Loading in sounds
        self.turret_rot_sound = THUDSOUND
        self.turret_rot_sound.set_volume(turret_rot_volume)
        self.fence_collision_sound = pg.mixer.Sound(fence_collision_path)
        self.fence_collision_sound.set_volume(fence_collision_volume)
        self.engine_sound = pg.mixer.Sound(engine_sound_path)

    def apply_movement(self): #Apply the current velocity (self.angle as direction, self.speed as magnitude)
        x_change = self.speed * math.cos(self.angle) * self.game.delta_time
        y_change = self.speed * math.sin(-self.angle) * self.game.delta_time

        #Check for collisions. If there exist collisions, (evident by deflectionSpeed being positive) then apply the calculated deflection velocity.
        if self.deflectionSpeed > 0:
            x_change += self.deflectionSpeed * math.cos(self.deflectionAngle) * self.game.delta_time
            y_change += self.deflectionSpeed * math.sin(-self.deflectionAngle) * self.game.delta_time

            #Decelerating the deflection speed, so the bounce "dies out" due to friction.
            self.deflectionSpeed *= 1 - (bounceDeceleration * self.game.delta_time)
            if abs(self.deflectionSpeed) < accelsens: #If the deflection speed is low enough, stop calculating for deflection velocity.
                self.deflectionSpeed = 0

        #Throttle if max speed is reached.
        if self.speed > player_max_speed: 
            self.speed = player_max_speed
        if self.speed < -player_max_speed:
            self.speed = -player_max_speed

        #Check for collisions before applying movement.
        if self.check_wall(int(self.x + x_change),int(self.y)): #If not colliding with a wall on the x axis,
            self.x += x_change #Then apply for that axis
        if self.check_wall(int(self.x),int(self.y+y_change)):
            self.y += y_change


        #Pixel-based collisions for the obstacles
    
    def checkCollision(self): #Detects for pixel-based collisions between the tank sprite and anything in self.collidables, then returns the deflection angle.
        for group in self.collidables: 
            collisions = pg.sprite.spritecollide(self, group, False)
            if len(collisions) == 0: #If there are no objects colliding, 
                continue
            else: #Otherwise, do all this calculation stuff.
                for collision in collisions:
                    if id(collision) == id(self): #The tank shouldn't calculate collisions with itself. Move on to the next collision of this group.
                        continue

                    pg.draw.rect(self.game.screen, 'blue', collision.rect, 3)
                    
                    maskCollisionPoint = pg.sprite.collide_mask(self, collision) #The x and y coordinate of the collision, in the local space of the mask's rectangle (top corner of the rectangle is 0,0)
                    if maskCollisionPoint == None:
                        continue #If collide_mask returns None, then there is no collision to calculate.

                    self.game.screen.set_at(maskCollisionPoint, 'blue')
                    self.game.screen.blit(self.mask.to_surface(), self.mask.get_rect())

                    #Find that intersecting point in world game space.
                    x = self.rect.left + maskCollisionPoint[0] #Calculating the local space coordinate transposed onto world space. self.rect is the rectangle for the tank sprite.
                    y = self.rect.top + maskCollisionPoint[1]
                    pg.draw.rect(self.game.screen, 'blue', pg.Rect(x, y, 5,5)) #Helper function to draw where that collision was.

                    #Getting the angle of the collision point to the center of the tank.

                    if (self.xDisplay - x) == 0: #If the collision point is at the center of the tank, then don't calculate the rest. It's useless and will create an error.
                        continue
                    
                    collision_point_angle = math.atan((self.yDisplay - y) / (self.xDisplay - x))
                    pg.draw.line(self.game.screen, 'green', (self.xDisplay, self.yDisplay), (self.xDisplay + math.cos(collision_point_angle) * COORDINATEMULTX, self.yDisplay + math.sin(-collision_point_angle) * COORDINATEMULTY), 2)

                    #Correct the angle for each quadrant, because arctan is restricted and is also stupid.
                    if (self.yDisplay > y) and (self.xDisplay < x): #Q1
                        collision_point_angle = -collision_point_angle
                    if (self.yDisplay > y) and (self.xDisplay > x): #Q2
                        collision_point_angle = math.pi - collision_point_angle
                    if (self.yDisplay < y) and (self.xDisplay > x): #Q3
                        collision_point_angle = math.pi + abs(collision_point_angle)
                    if (self.yDisplay < y) and (self.xDisplay < x): #Q4  
                        collision_point_angle = -(collision_point_angle) #If not in Q3, then it's in Q2
                    collision_point_angle %= 2 * math.pi
                    
                    #Get the inverse of the bisecting angle between the tank's angle and the collision angle.

                    #Creating a copy of self.angle.
                    if self.speed < 0: #If the tank is reversing,
                        tankAngle = (self.angle + math.pi) % (2 * math.pi)
                    else:
                        tankAngle = self.angle

                    if self.angle > collision_point_angle:
                        greater = tankAngle; lesser = collision_point_angle
                    else:
                        greater = collision_point_angle; lesser = tankAngle
                    deflect_angle = lesser + ((greater - lesser) / 2)
                    if (greater - lesser) < math.pi:
                        deflect_angle += math.pi
                    
                    #Setting the deflection variables to be used by self.apply_movement.
                    if abs(self.speed) > minimumBounceSpeed: #Deflections should always have a velocity, otherwise Tanks will not bounce when they rotate into surfaces.
                        self.deflectionSpeed = (abs(self.speed) * bounceSpeedFactor)
                    elif abs(self.speed) > player_max_speed: #Deflections should be less than a player's maximum velocity.
                        self.deflectionSpeed = player_max_speed
                    else:
                        self.deflectionSpeed = minimumBounceSpeed
                    self.deflectionAngle = deflect_angle
                    
                    pg.draw.rect(self.game.screen, 'blue', pg.Rect(maskCollisionPoint[0], maskCollisionPoint[1], 2,2))
                    
                    #Red is the tank's forward velocity, blue is the angle of collision, green is the unprocessed angle of collision, and purple is the calculated angle of deflection.
                    pg.draw.line(self.game.screen, 'blue', (self.xDisplay, self.yDisplay), (self.xDisplay + math.cos(collision_point_angle) * COORDINATEMULTX, self.yDisplay + math.sin(-collision_point_angle) * COORDINATEMULTY), 2)
                    pg.draw.line(self.game.screen, 'red', (self.xDisplay, self.yDisplay), (self.xDisplay + (math.cos(self.angle) * COORDINATEMULTX), self.yDisplay + (math.sin(-self.angle) * COORDINATEMULTY)), 2) #Forward velocity
                    pg.draw.line(self.game.screen, 'purple', (self.xDisplay, self.yDisplay), (self.xDisplay + math.cos(deflect_angle) * COORDINATEMULTX, self.yDisplay + math.sin(-deflect_angle) * COORDINATEMULTY), 2) #deflection angle

                    

                    return True, collision
        return False, None #If there are no objects colliding, then return False also.

    def check_wall(self,x,y): #Check for wall collision by comparing that point with the world_map.
        return ((x,y) not in self.game.map.world_map) and (0 < x < 16 and 0 < y < 9)

    
    def destroy(self):
        DeadTank(self.game, self.rect.center)
        print(str(self), 'has died.') #I'm leaving this here just in case, but in order for this to work properly, both the NPC and Player class need a __str__ method
        self.kill()

    # Method to update the tank's state
    def update(self):
        self.isColliding = self.checkCollision()
        
        if not self.stopped:
            self.apply_movement() #Apply any movement to the objects x and y
            self.rect.center = (self.xDisplay, self.yDisplay)  # Update sprite's position to new x and y

    # Method to draw the tankbody and turret, correctly rotated. Also updates the mask for collisions.
    def draw(self):
        self.xDisplay = self.x * COORDINATEMULTX
        self.yDisplay = self.y * COORDINATEMULTY
        
        #Tank body
        rotated_image = pg.transform.rotate(self.image, math.degrees(self.angle))
        self.rect = rotated_image.get_rect(center=(self.xDisplay, self.yDisplay))
        rotated_image = pg.transform.rotate(self.image, math.degrees(self.angle))
        self.rect = rotated_image.get_rect(center=(self.xDisplay, self.yDisplay))
        self.mask = pg.mask.from_surface(rotated_image)
        self.game.screen.blit(rotated_image, self.rect)
        
        #Turret
        rotated_turret = pg.transform.rotate(self.turret_image, math.degrees(self.turret_angle))
        turret_rect = rotated_turret.get_rect(center=(self.xDisplay, self.yDisplay))
        rotated_turret = pg.transform.rotate(self.turret_image, math.degrees(self.turret_angle))
        turret_rect = rotated_turret.get_rect(center=(self.xDisplay, self.yDisplay))
        self.game.screen.blit(rotated_turret, turret_rect)
        
    # Property to get the tank's position
    @property
    def pos(self):
        return self.x, self.y

    # Property to get the tank's position as integers
    @property
    def map_pos(self):
        return int(self.x), int(self.y)
    
    @property
    def display_pos(self):
        return self.xDisplay, self.yDisplay