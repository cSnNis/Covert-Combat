import pygame as pg
from pygame import mixer
import sys
import random
from settings import *
from map import *
from player import *
import DebuggingDisplay

class Game:
  #initiating and defining everthing made so far
  def __init__(self):
    pg.mixer.pre_init(44100, -16, 1, 512)
    pg.init()
    pg.mixer.init()
    self.screen = pg.display.set_mode(res)
    self.delta_time = 1
    self.clock = pg.time.Clock()
    self.new_game()
    
  def new_game(self):
    self.map = Map(self)
    self.shell_group = pg.sprite.Group()
    self.player = Player(self,p1Inputs)

    self.debug = DebuggingDisplay.DebugDisplay(self)

    mixer.music.load('BattleMusic.mp3')
    mixer.music.set_volume(.25)

  def update(self):
    self.player.update()
    self.debug.update()
    pg.display.flip()
    self.delta_time = self.clock.tick(fps) / 1000
    pg.display.set_caption(f'{self.clock.get_fps() :.1f}')
    
  def draw(self):
    self.screen.fill('black')
    self.map.draw()
    self.player.draw()
    self.shell_group.draw(self.screen)

    self.debug.draw()

  def check_events(self):
    for event in pg.event.get():
      if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
        pg.quit()
        sys.exit()
      if event.type == pg.KEYDOWN and event.key == pg.K_m:
        if mixer.music.get_busy() == False:
          mixer.music.play(-1)
        else:
          mixer.music.stop()
    
  def run(self):
    while True:
      self.check_events()
      self.update()
      self.draw()
  
      
  
if __name__ == '__main__':
  game = Game()
  game.run()
  