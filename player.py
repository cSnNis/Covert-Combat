from settings import *
import pygame as pg
import math
class player:
  def __init__(self,game):
    self.game = game
    self.x, self.y = player_pos
    self.angle = player_angle
    self.x_change = x_change
    self.y_change = y_change
    self.accelerating = False
  def movement(self):
    sin_a = math.sin(self.angle)
    cos_a = math.cos(self.angle)
    dx, dy = 0, 0
    speed = player_accel * self.game.delta_time
    speed_sin = speed * sin_a
    speed_cos = speed * cos_a
    keys = pg.key.get_pressed()
    if keys[pg.K_w]:
      self.x_change += speed_cos
      self.y_change += speed_sin
      dx += self.x_change
      dy += self.y_change
      self.accelerating = True
    if keys[pg.K_s]:
      self.x_change -= speed_cos
      self.y_change -= speed_sin
      dx += self.x_change
      dy += self.y_change
      self.accelerating = True
    else:
      self.accelerating = False
      self.x_change *= 0.5
      self.y_change *= 0.5
      max_speed = 1
      magnitude = math.sqrt(self.x_change**2 + self.y_change**2)
      if magnitude > max_speed:
          scaling_factor = max_speed / magnitude
          self.x_change *= scaling_factor
          self.y_change *= scaling_factor
    self.check_wall_collision(dx, dy)

    if keys[pg.K_LEFT]:
      self.angle -= player_rot_speed * self.game.delta_time
    if keys[pg.K_RIGHT]:
      self.angle += player_rot_speed * self.game.delta_time
    self.angle %= math.tau
  def check_wall(self,x,y):
    return(x,y) not in self.game.map.world_map
  def check_wall_collision(self,dx,dy):
    if self.check_wall(int(self.x+dx),int(self.y)):
      self.x += dx
    if self.check_wall(int(self.x),int(self.y+dy)):
      self.y += dy

  def draw(self):
    pg.draw.line(self.game.screen, 'red', (self.x *100, self.y * 100), 
                 (self.x * 100 + WIDTH * math.cos(self.angle),
                 self.y * 100 + WIDTH * math.sin(self.angle)), 2)
    pg.draw.rect(self.game.screen,'red', pg.Rect(self.x*100 , self.y*100 , 10, 10))
  

  def update(self):
    self.movement()
  @property
  def pos(self):
    return self.x, self.y
  @property
  def map_pos(self):
    return int(self.x), int(self.y)