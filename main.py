import pygame as pg
import sys
import random
from settings import *
from map import *
from player import *
from NPC import *
import DebuggingDisplay

class Game:
  #initiating and defining everthing made so far
  def __init__(self):
    pg.init()
    pg.mixer.init()
    self.screen = pg.display.set_mode(res)
    self.delta_time = 1
    self.clock = pg.time.Clock()
    self.bg_music = pg.mixer.music
    self.soundMixer = pg.mixer
    
    self.new_game()
    
  def new_game(self):
    self.map = Map(self)
    
    self.shell_group = pg.sprite.Group()

    #Spawning in the players.
    self.p1 = Player(self,p1Inputs)
    self.p2 = Player(self, p2Inputs)

    #Spawning in the NPC's
    for i in range(5):
      NPC(self, (i,i), i)

    self.debug = DebuggingDisplay.DebugDisplay(self)

    self.bg_music.load('TTFAFmusic.mp3')
    self.bg_music.set_volume(.25)
    self.bg_music.play()

  def update(self):
    self.p1.update()
    self.debug.update()
    pg.display.flip()
    self.delta_time = self.clock.tick(fps) / 1000
    pg.display.set_caption(f'{self.clock.get_fps() :.1f}')
    
  def draw(self):
    self.screen.fill('black')
    self.map.draw()
    self.p1.draw()
    self.shell_group.draw(self.screen)

    self.debug.draw()

  def check_events(self):
    for event in pg.event.get():
      if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
        pg.quit()
        sys.exit()
    
  def run(self):
    self.bg_music.play(-1)
    while True:
      self.check_events()
      self.update()
      self.draw()
  
      
  
if __name__ == '__main__':
  game = Game()
  game.run()
  