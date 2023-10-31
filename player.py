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
      self.tank_rect = self.image.get_rect(center=(self.x * 150, self.y * 50))
      self.dx, self.dy = 0, 0

    def movement(self):
      sin_a = math.sin(self.angle)
      cos_a = math.cos(self.angle)
      keys = pg.key.get_pressed()
      if keys[pg.K_LEFT]:
        self.angle -= player_rot_speed * self.game.delta_time
      if keys[pg.K_RIGHT]:
        self.angle += player_rot_speed * self.game.delta_time

        # Calculate the adjusted speed based on direction
      speed_x = player_speed * cos_a
      speed_y = player_speed * sin_a
      if keys[pg.K_w]:
            # Accelerate forward
        self.dx += speed_x
        self.dy += speed_y
        self.accelerating = True
        magnitude = math.sqrt(self.dx**2 + self.dy**2)
        if magnitude > player_max_speed:
          scaling_factor = player_max_speed / magnitude
          self.dx *= scaling_factor
          self.dy *= scaling_factor
      elif keys[pg.K_s]:
            # Decelerate (apply braking)
        self.dx -= speed_x
        self.dy -= speed_y
        self.accelerating = True
        magnitude = math.sqrt(self.dx**2 + self.dy**2)
        if magnitude > player_max_speed:
          scaling_factor = (player_max_speed / 2) / magnitude
          self.dx *= scaling_factor
          self.dy *= scaling_factor
      else:
            # Apply deceleration
          deceleration = player_deceleration * self.game.delta_time
          self.dx -= min(deceleration, abs(self.dx)) * (self.dx / abs(self.dx) if self.dx != 0 else 1)
          self.dy -= min(deceleration, abs(self.dy)) * (self.dy / abs(self.dy) if self.dy != 0 else 1)
          self.accelerating = False
      self.x += self.dx
      self.y += self.dy
  
    def update(self):
        self.movement()

    def draw(self):
    #finding the center of the tank
      self.tank_rect.center = (self.x * 150, self.y * 50)
      #defining the rotated image
      rotated_image = pg.transform.rotate(self.image, math.degrees(-self.angle))
      #getting the rotated image
      self.tank_rect = rotated_image.get_rect(center=self.tank_rect.center)
      #drawing and placeing the new rotated image
      self.game.screen.blit(rotated_image, self.tank_rect)
class turret:
  #creat turret movement and shooting here
    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)