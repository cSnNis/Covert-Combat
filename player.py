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

        self.image = pg.image.load(tank_sprite_path).convert_alpha()  # Load player image
        self.rect = self.image.get_rect()  # Create a rect for the player sprite
        self.rect.center = (self.x * COORDINATEMULTX, self.y * COORDINATEMULTY)  # Set the initial position
        self.dx, self.dy = 0, 0  # Initialize speed components
        self.speed = 0
        
        self.turret_angle = 0  # Initial turret angle
        self.turret_image = pg.image.load(turret_sprite_path).convert_alpha()  # Load turret image
        
        self.mask = pg.mask.from_surface(self.image) # We are only doing collisions for the body of the tank.

        self.stopped = True

    # Method to handle player movement
    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        keys = pg.key.get_pressed()

        if keys[pg.K_a]:
            self.angle -= player_rot_speed * self.game.delta_time  # Rotate left

        if keys[pg.K_d]:
            self.angle += player_rot_speed * self.game.delta_time  # Rotate right

        if keys[pg.K_q]:
            self.turret_angle -= player_rot_speed * self.game.delta_time  # Rotate turret left

        if keys[pg.K_e]:
            self.turret_angle += player_rot_speed * self.game.delta_time  # Rotate turret right

        speed_x = player_speed * cos_a
        speed_y = player_speed * sin_a

        if keys[pg.K_w]:  # Move forward
            self.dx += speed_x
            self.dy += speed_y
            self.accelerating = True
            magnitude = math.sqrt(self.dx ** 2 + self.dy ** 2)

            if magnitude > player_max_speed:
                scaling_factor = player_max_speed / magnitude
                self.dx *= scaling_factor
                self.dy *= scaling_factor
            collisions = pg.sprite.spritecollide(self, self.game.map.walls, False)
            if collisions:
                # Calculate dot products between movement vectors and wall normals
              self.dx = -self.dx 
              self.dy = -self.dy 

        elif keys[pg.K_s]:  # Move backward
            self.dx -= speed_x
            self.dy -= speed_y
            self.accelerating = True
            magnitude = math.sqrt(self.dx ** 2 + self.dy ** 2)

            if magnitude > player_max_speed:
                scaling_factor = (player_max_speed / 2) / magnitude
                self.dx *= scaling_factor
                self.dy *= scaling_factor
            collisions = pg.sprite.spritecollide(self, self.game.map.walls, False)
            if collisions:
                  # Calculate dot products between movement vectors and wall normals
                self.dx = -self.dx 
                self.dy = -self.dy
            

        else:  # Deceleration when no movement keys are pressed
            deceleration = player_deceleration * self.game.delta_time
            self.dx -= min(deceleration, abs(self.dx)) * (self.dx / abs(self.dx) if self.dx != 0 else 1)
            self.dy -= min(deceleration, abs(self.dy)) * (self.dy / abs(self.dy) if self.dy != 0 else 1)
            self.accelerating = False

        self.x += self.dx  # Update player's x position
        self.y += self.dy  # Update player's y position

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
            self.angle -= player_rot_speed * self.game.delta_time
            self.angle %= math.tau # To keep the player angle below 2pi. Clever.
        if keys[pg.K_d]:
            self.angle += player_rot_speed * self.game.delta_time
            self.angle %= math.tau 

        if keys[pg.K_q]: #Turret turning
            self.turret_angle -= player_rot_speed * self.game.delta_time
            self.turret_angle %= math.tau 
        if keys[pg.K_e]:
            self.turret_angle += player_rot_speed * self.game.delta_time
            self.turret_angle %= math.tau 

    def apply_movement(self): #Apply the current velocity (self.angle as direction, self.speed as magnitude)
        self.x_change = self.speed * math.cos(self.angle) * self.game.delta_time
        self.y_change = self.speed * math.sin(self.angle) * self.game.delta_time

        #Throttle if max speed is reached.
        if self.speed > player_max_speed: 
            self.speed = player_max_speed

        #Check for collisions before applying movement.
        # if self.check_wall(int(self.x + self.x_change),int(self.y)): #If not colliding with a wall on the x axis,
        #     self.x += self.x_change #Then apply for that axis
        # if self.check_wall(int(self.x),int(self.y+self.y_change)):
        #     self.y += self.y_change

        #Sprite-based collisions
        collisions = pg.sprite.spritecollide(self, self.game.map.walls, False)
        if not collisions:
            # Calculate dot products between movement vectors and wall normals
            self.x += self.x_change #Then apply for that axis
            self.y += self.y_change

    def check_wall(self,x,y): #Check for wall collision by comparing that point with the world_map.
        return(x,y) not in self.game.map.world_map

    # Method to update the player's state
    def update(self):
        #self.movement()  # Call movement method to handle movement
        self.get_movement()
        self.apply_movement()
        self.rect.center = (self.x * 200, self.y * 50)  # Update sprite's position
        #self.draw()  # Call draw method to render the player and turret

    # Method to draw the player and turret
    def draw(self):
        xDisplay = self.x * COORDINATEMULTX
        yDisplay = self.y * COORDINATEMULTY
        
        #Tank body
        rotated_image = pg.transform.rotate(self.image, math.degrees(-self.angle))
        self.rect = rotated_image.get_rect(center=(xDisplay, yDisplay))
        self.mask = pg.mask.from_surface(rotated_image)
        self.game.screen.blit(rotated_image, self.rect)
        
        #Turret
        rotated_turret = pg.transform.rotate(self.turret_image, math.degrees(-self.turret_angle))
        turret_rect = rotated_turret.get_rect(center=(xDisplay, yDisplay))
        self.game.screen.blit(rotated_turret, turret_rect)

    # Property to get the player's position
    @property
    def pos(self):
        return self.x, self.y

    # Property to get the player's position as integers
    @property
    def map_pos(self):
        return int(self.x), int(self.y)