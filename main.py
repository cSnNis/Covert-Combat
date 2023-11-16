import pygame as pg
import sys
import random
from settings import *
from map import *
from player import *
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
    self.bg_image = pg.transform.scale(pg.image.load('sand.png'), res)
    self.bg_rect = self.bg_image.get_rect(topleft = (0,0))
    
    self.new_game()
    
  def new_game(self):
    self.map = Map(self)
    self.player_group = pg.sprite.Group()
    self.player = Player(self,p1Inputs)
    
    self.debug = DebuggingDisplay.DebugDisplay(self)

    self.bg_music.load('TTFAFmusic.mp3')
    self.bg_music.set_volume(.25)
    self.bg_music.play()


  def update(self):
    self.player.update()
    pg.display.flip()
    self.delta_time = self.clock.tick(fps)/1000
    pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    self.debug.update()
    
  def draw(self):
    self.screen.blit(self.bg_image, self.bg_rect)
    
    self.map.draw()
    self.player.draw()

    self.debug.draw()

  def check_events(self):
    for event in pg.event.get():
      if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
        pg.quit()
        sys.exit()
    
  def run(self):
    while True:
      self.check_events()
      self.update()
      self.draw()
  
      
  
if __name__ == '__main__':
  game = Game()
  game.run()
  