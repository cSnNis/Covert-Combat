from settings import *
import pygame as pg
import math
from main import *
from BaseTank import BaseTank
import random

# Define the Player class for the player character
class Player(BaseTank):
    def __init__(self, game, startPosition, startAngle, inputTuple):

        #Initialialize tank properties.
        super().__init__(game, game.player_group, startPosition, startAngle)

        self.inputs = inputTuple

        #For shooting
        self.shell_group = pg.sprite.Group()
        self.CooldownTimer = 2
        
        self.turretMovement = True

    def get_movement(self): #Get movement from the player.
        keys = pg.key.get_pressed() #dictionary of keys pressed this frame
        if keys[self.inputs[0]]: #Forward 
            if self.speed < 0: #If the tank is moving backward and is now trying to move forward, it should also deccelerate.
                self.speed *= 1 - (player_deceleration * self.game.delta_time)
            self.stopped = False
            self.speed += player_accel * self.game.delta_time            
            self.engine_sound.set_volume(self.speed/5)
            if self.engine_sound.get_num_channels() == 0:
                self.engine_sound.play(-1)
        elif keys[self.inputs[1]]: #Backward acceleration
            if self.speed > 0: #If the tank is moving forward and is now trying to move backward, then the tank should also deccelerate
                self.speed *= 1 - (player_deceleration * self.game.delta_time)
            self.stopped = False
            self.speed -= player_accel * self.game.delta_time
            self.engine_sound.set_volume(abs(self.speed)/5)
            if self.engine_sound.get_num_channels() == 0:                
                self.engine_sound.play(-1)
        else: #No inputs, begin decelerating
            if not self.stopped:
                if abs(self.speed) > accelsens:
                    self.speed *= 1 - (player_deceleration * self.game.delta_time)
                    self.engine_sound.set_volume(abs(self.speed)/5)
                else:
                    self.stopped = True
                    self.speed = 0
                    self.engine_sound.stop()
                    self.deflectionSpeed = 0

        if keys == pg.K_SPACE:
            shell = self.player.shoot() #attempts to create a shell object, if the limit was reached, no shell will be made
            if shell is not None: #if a shell was produced (there is either an shell object or None here)
              shell.add(self.shell_group)

        if keys[self.inputs[2]]: #Turning
            self.stopped = False
            self.angle += player_rot_speed * self.game.delta_time
        if keys[self.inputs[3]]:
            self.stopped = False
            self.angle -= player_rot_speed * self.game.delta_time
        self.angle %= math.tau 

        if keys[self.inputs[4]]: #Turret turning
            self.turret_angle += player_rot_speed * self.game.delta_time
            self.turret_angle %= math.tau 
        if keys[self.inputs[5]]:
            self.turret_angle -= player_rot_speed * self.game.delta_time
            self.turret_angle %= math.tau 
        
        self.CooldownTimer += self.game.delta_time
        if keys[self.inputs[6]]:
            if self.CooldownTimer > .2:
                self.CooldownTimer = 0
                self.shoot()
                #shell = self.shoot() #attempts to create a shell object, if the limit was reached, no shell will be made
                # if shell: #if a shell was produced (there is either an shell object or None here)
                #     self.shell_group.add(shell)

        if keys[self.inputs[5]] or keys[self.inputs[4]]:
            if self.turret_rot_sound.get_num_channels() == 0:
                self.turret_rot_sound.play(-1)
        else:
            self.turret_rot_sound.stop()

    def shoot(self): 
        if len(self.shell_group) <= 5: #If there are more than 6 shells on screen, don't create another
            Shell(self.game, self.rect.centerx, self.rect.centery, self).add(self.shell_group) #Makes a shell that shoots from center of the top side
            print('Bullet shot, there are ' + str(len(self.shell_group)))

    # Override of the basetank method, which updates the shells also.
    def update(self):
        self.get_movement() #Get any player inputs, and apply them to movement variables.

        super().update()

        self.shell_group.update()

    # Override of the BaseTank method, which also draws the shells.
    def draw(self):
        super().draw()

        self.shell_group.draw(self.game.screen)


#Bullet/Shell Class
class Shell(pg.sprite.Sprite):
    def __init__(self, game, x, y, player):
        super().__init__()
        self.game = game
        self.player = player
        self.angle = player.turret_angle
        self.image = pg.transform.scale_by(pg.image.load(shell_sprite_path).convert_alpha(),.01)  #create an image object (essentially a surface), rotated as the turret is.
        self.image = pg.transform.rotate(self.image, math.degrees(self.angle))
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center = (x,y)) #make a shell that's center lies where the player is
        self.collidables = [self.game.map.walls, self.game.player_group]
        self.speed = 500 #If you adjust the speed, keep it within the hundreds range

    def update(self):
        x_change = self.speed * math.cos(self.angle) * self.game.delta_time #uses the same angle calculations as the player's turret
        y_change = self.speed * math.sin(-self.angle) * self.game.delta_time
        self.rect.centerx += x_change #moves the center every time it updates
        self.rect.centery += y_change
        self.checkCollision() #checks to see if hit something afer moving
        
    def checkCollision(self): #Detects for pixel-based collisions between this sprite and anything in group self.collidables, returns the name of the collided object and it's point in display space.
        for group in self.collidables:
            collisions = pg.sprite.spritecollide(self, group, False)
            if len(collisions) > 0: #If there exists a collision, 
                collision = collisions[0] #Only calculate the first object of this group.

                if id(collision) == id(self.player): #The tank shouldn't calculate collisions with itself.
                    if len(collisions) > 1:
                        collision = collisions[1]
                    else:
                        continue

                maskCollisionPoint = pg.sprite.collide_mask(self, collision) #The x and y coordinate of the collision, in the local space of the mask's rectangle (top corner of the rectangle is 0,0)

                if maskCollisionPoint == None:
                    continue #If collide_mask returns None, then there is no collision to calculate.

                print("COLLIDED WITH " + str(collision))
                self.kill()

                #Find that intersecting point in world game space.
                x = self.rect.left + maskCollisionPoint[0] #Calculating the local space coordinate transposed onto world space. self.rect is the rectangle for the tank sprite.
                y = self.rect.top + maskCollisionPoint[1]

                pg.draw.rect(self.game.screen, 'blue', pg.Rect(x, y, 5,5)) #Helper function to draw where that collision was.

                return True, collision, (x,y)
        return False, None, (0,0) #If there are no objects colliding, then return False also.

