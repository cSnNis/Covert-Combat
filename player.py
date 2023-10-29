from settings import *
import pygame as pg
import math
from map import *

class Player:
    def __init__(self, game):
      self.game = game
      self.x, self.y = player_pos
      self.angle = player_angle
      self.image = pg.image.load('download (9) (2).png').convert_alpha()
      self.tank_rect = self.image.get_rect(center=(self.x * 150, self.y * 100))
      self.dx, self.dy = 0, 0

    def movement(self):
      sin_a = math.sin(self.angle)
      cos_a = math.cos(self.angle)
      speed = player_speed * self.game.delta_time
      keys = pg.key.get_pressed()


      if keys[pg.K_LEFT]:
        self.angle += player_rot_speed * self.game.delta_time
      if keys[pg.K_RIGHT]:
        self.angle -= player_rot_speed * self.game.delta_time

      if keys[pg.K_w]:
        # Accelerate forward
        self.dx += speed * cos_a
        self.dy -= speed * sin_a
        self.accelerating = True
        magnitude = math.sqrt(self.dx**2 + self.dy**2)
        if magnitude > player_max_speed:
            scaling_factor = player_max_speed / magnitude
            self.dx *= scaling_factor
            self.dy *= scaling_factor
      elif keys[pg.K_s]:
      # Decelerate (apply braking)
        self.dx -= speed * cos_a
        self.dy += speed * sin_a
        self.accelerating = True
        magnitude = math.sqrt(self.dx**2 + self.dy**2)
        if magnitude > player_max_speed:
            scaling_factor = (player_max_speed/2) / magnitude
            self.dx *= scaling_factor
            self.dy *= scaling_factor
      else:
        # Apply deceleration
        deceleration = player_deceleration * self.game.delta_time
        self.dx -= min(deceleration, abs(self.dx)) * (self.dx / abs(self.dx) if self.dx != 0 else 1)
        self.dy -= min(deceleration, abs(self.dy)) * (self.dy/ abs(self.dy) if self.dy != 0 else 1)
        self.accelerating = False

      self.x += self.dx
      self.y += self.dy
    
    def check_wall(self,x,y):
      return(x,y) not in self.game.world_map

    def check_wall_collision(self,dx,dy):
      if self.check_wall(int(self.x+dx),int(self.y)):
        pg.quit()
      if self.check_wall(int(self.x),int(self.y+dy)):
        pg.quit()
  
    def update(self):
        self.movement()
        # Add code for bullet logic here

    def draw(self):
      self.tank_rect.center = (self.x * 150, self.y * 100)
      rotated_image = pg.transform.rotozoom(self.image, math.degrees(self.angle), 1)
      self.game.screen.blit(rotated_image, self.tank_rect.topleft)

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)