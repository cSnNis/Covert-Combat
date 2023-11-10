from settings import *
import pygame as pg
import math

# Define the Player class for the player character
class Player(pg.sprite.Sprite):
    def __init__(self, game):
        # Initialize the player's attributes
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.x, self.y = player_pos  # Initial player position
        self.angle = player_angle  # Initial player angle

        self.xDisplay, self.yDisplay = (self.pos[0] * COORDINATEMULT[0], self.pos[1] * COORDINATEMULT[1])
        self.image = pg.image.load(tank_sprite_path).convert_alpha(); self.image = pg.transform.scale(self.image, (self.image.get_width() * RESMULTX * tankSpriteScalingFactor, self.image.get_height() * RESMULTY * tankSpriteScalingFactor))  # Load player image, scale it by the set scaling factor and the set resolution.
        self.rect = self.image.get_rect()  # Create a rect for the player sprite
        self.rect.center = (self.x * COORDINATEMULTX, self.y * COORDINATEMULTY)  # Set the initial position
        self.dx, self.dy = 0, 0  # Initialize speed components
        self.speed = 0
        
        self.turret_angle = 0  # Initial turret angle
        self.turret_image = pg.image.load(turret_sprite_path).convert_alpha(); self.turret_image = pg.transform.scale(self.turret_image, (self.turret_image.get_width() * RESMULTX * tankSpriteScalingFactor, self.turret_image.get_height() * RESMULTY * tankSpriteScalingFactor))  # Load turret image
        
        #Collision Variables
        self.collidables = [self.game.map.walls] #Anything that should be collided with should be in this group.
        self.mask = pg.mask.from_surface(self.image) # We are only doing collisions for the body of the tank.
        self.isColliding = (False, 0)
        self.deflectionSpeed = 0

        self.stopped = True

    def get_movement(self): #Get movement from the player.
        keys = pg.key.get_pressed() #dictionary of keys pressed this frame
        if keys[pg.K_w]: #Forward 
            if self.speed < 0: #If the tank is moving backward and is now trying to move forward, it should also deccelerate.
                self.speed *= 1 - (player_deceleration * self.game.delta_time)
            self.stopped = False
            self.speed += player_accel * self.game.delta_time
        elif keys[pg.K_s]: #Backward acceleration
            if self.speed > 0: #If the tank is moving forward and is now trying to move backward, then the tank should also deccelerate
                self.speed *= 1 - (player_deceleration * self.game.delta_time)
            self.stopped = False
            self.speed -= player_accel * self.game.delta_time
        else: #No input, begin decelerating
            if not self.stopped:
                if abs(self.speed) > accelsens:
                    self.speed *= 1 - (player_deceleration * self.game.delta_time)
                else:
                    self.stopped = True
                    self.speed = 0

        if keys[pg.K_a]: #Turning
            self.stopped = False
            self.angle += player_rot_speed * self.game.delta_time
            self.angle %= math.tau # To keep the player angle below 2pi. Clever.
        if keys[pg.K_d]:
            self.stopped = False
            self.angle -= player_rot_speed * self.game.delta_time
            self.angle %= math.tau 

        if keys[pg.K_q]: #Turret turning
            self.turret_angle += player_rot_speed * self.game.delta_time
            self.turret_angle %= math.tau 
        if keys[pg.K_e]:
            self.turret_angle -= player_rot_speed * self.game.delta_time
            self.turret_angle %= math.tau 

    def apply_movement(self): #Apply the current velocity (self.angle as direction, self.speed as magnitude)
        x_change = self.speed * math.cos(self.angle) * self.game.delta_time
        y_change = self.speed * math.sin(-self.angle) * self.game.delta_time

        #Check for collisions. If there exist collisions, (evident by deflectionSpeed being positive) then apply the calculated deflection velocity.
        self.checkCollision()
        if self.deflectionSpeed > 0:
            x_change += self.deflectionSpeed * math.cos(self.deflectionAngle) * self.game.delta_time
            y_change += self.deflectionSpeed * math.sin(-self.deflectionAngle) * self.game.delta_time

            #Decelerating the deflection speed, so the bounce "dies out" due to friction.
            self.deflectionSpeed *= 1 - (player_deceleration * self.game.delta_time)
            if abs(self.deflectionSpeed) < accelsens: #If the deflection speed is low enough, stop calculating for deflection velocity.
                self.deflectionSpeed = 0

        #Throttle if max speed is reached.
        if self.speed > player_max_speed: 
            self.speed = player_max_speed

        #Check for collisions before applying movement.
        if self.check_wall(int(self.x + x_change),int(self.y)): #If not colliding with a wall on the x axis,
            self.x += x_change #Then apply for that axis
        if self.check_wall(int(self.x),int(self.y+y_change)):
            self.y += y_change


        #Pixel-based collisions for the obstacles
    def checkCollision(self): #Detects for pixel-based collisions between the tank sprite and anything in self.collidables, then returns the deflection angle.
        for group in self.collidables: 
            collisions = pg.sprite.spritecollide(self, group, False)
            if len(collisions) > 0: #If there exists a collision, 
                collision = collisions[0] #Only calculate the first, so far.
                
                maskCollisionPoint = pg.sprite.collide_mask(self, collision) #The x and y coordinate of the collision, in the local space of the mask's rectangle (top corner of the rectangle is 0,0)
                if maskCollisionPoint == None:
                    return False, None #If collide_mask returns None, then there is no collision to calculate.

                self.game.screen.set_at(maskCollisionPoint, 'blue')
                self.game.screen.blit(self.mask.to_surface(), self.mask.get_rect())

                #Find that intersecting point in world game space.
                x = self.rect.left + maskCollisionPoint[0] #Calculating the local space coordinate transposed onto world space. self.rect is the rectangle for the tank sprite.
                y = self.rect.top + maskCollisionPoint[1]
                pg.draw.rect(self.game.screen, 'blue', pg.Rect(x, y, 5,5)) #Helper function to draw where that collision was.

                #Getting the angle of the collision point to the center of the tank.
                
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
                if self.angle > collision_point_angle:
                    greater = self.angle; lesser = collision_point_angle
                else:
                    greater = collision_point_angle; lesser = self.angle
                deflect_angle = lesser + ((greater - lesser) / 2)
                if (greater - lesser) < math.pi:
                    deflect_angle += math.pi
                
                #Setting the deflection variables to be used by self.apply_movement.
                if abs(self.speed) > accelsens: #Deflections should always have a velocity, otherwise Tanks will not bounce when they rotate into surfaces.
                    self.deflectionSpeed = (abs(self.speed) * 1)
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
        return(x,y) not in self.game.map.world_map

    def shoot(self): #does not include angle right now, bullets will always shoot up
        if len(shell_group) >= 6:
            return None #something must be returned or it will cause an error down the line
        else:
            shell = Shell(self.rect.centerx, self.rect.top) #Makes a bullet that shoots from center of the top side
            return shell    

    # Method to update the player's state
    def update(self):
        self.get_movement() #Get player inputs

        if not self.stopped: 
            self.apply_movement() #Apply the movement

        self.rect.center = (self.x * 200, self.y * 50)  # Update sprite's position

    # Method to draw the player and turret
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

        pg.draw.line(self.game.screen, 'red', (self.xDisplay, self.yDisplay), (self.xDisplay + (math.cos(self.angle) * COORDINATEMULTX), self.yDisplay + (math.sin(-self.angle) * COORDINATEMULTY)), 2) #Forward velocity

    # Property to get the player's position
    @property
    def pos(self):
        return self.x, self.y

    # Property to get the player's position as integers
    @property
    def map_pos(self):
        return int(self.x), int(self.y)
    @property
    def display_pos(self):
        return self.xDisplay, self.yDisplay


#Bullet/Shell Class
class Shell(pg.sprite.Sprite):
    def __init__(self, px, py):
        super().__init__()
        self.image = pg.Surface((10, 20)) #create an image object (essentially a surface)
        self.image.fill(225,255,0) #Yellow
        self.rect = self.image.get_rect(center = (px, py)) #make a bullet that's center lies where the player is
    def update(self):
        self.rect.move_ip(0, -5)
    def detect_wall(self, collision):
        for shell in collision.keys():
            shell_group.remove(shell)

shell_group = pg.sprite.Group()