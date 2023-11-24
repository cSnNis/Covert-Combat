import pygame as pg
from pygame import mixer
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
    pg.mixer.pre_init(44100, -16, 1, 512)
    pg.init()
    pg.mixer.init()
    self.screen = pg.display.set_mode(res)
    self.delta_time = 1
    self.clock = pg.time.Clock()

    self.bg_music = pg.mixer.music
    self.soundMixer = pg.mixer
    self.bg_image = pg.transform.scale(pg.image.load('images/obstacles/sand.png'), res)
    self.bg_rect = self.bg_image.get_rect(topleft = (0,0))

  def start_menu(self): #Displaying the start menu. It acts as it's own gameloop, so Game.new_game() is not called until it breaks.
    pg.display.set_caption('COVERT COMBAT')

    #Loading in music.
    self.bg_music.load(start_music_path)
    self.bg_music.set_volume(.25)
    self.bg_music.play()

    #Loading in the splash art and logo
    splashImage = pg.transform.scale(pg.image.load(splash_image_path), res) #The overall image. Everything to be on screen should be blitted onto this image.
    logoImage = pg.transform.scale(pg.image.load(logo_image_path), res)
    splashImage.blit(logoImage, logoImage.get_rect(center = (res[0]/2,res[1]/4)))

    #Adding Logo/instructions to the splash art.
    if not pg.font.get_init(): #If the font module is not initialized, 
      pg.font.init() #Initialize it. 
    start_font = pg.font.Font(start_font_path,30)
    yaddition = 300 * RESMULTY
    for line in start_instructions: #Print out each line of the starting instructions.
      instructionsImageUnscaled = start_font.render(line, True, 'white', 'black')
      instructionsImage = pg.transform.scale(instructionsImageUnscaled, (instructionsImageUnscaled.get_rect().width * RESMULTX,instructionsImageUnscaled.get_rect().height * RESMULTY))
      splashImage.blit(instructionsImage, instructionsImage.get_rect(center=(res[0]/2,res[1]/2 + yaddition)))
      yaddition += 35 * RESMULTY

    #Finally, draw the completed splash art. 
    self.screen.blit(splashImage, splashImage.get_rect(topleft = (0,0)))
    pg.display.flip()

    while True: #Wait until a key is pressed to exit. 
      for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
          pg.quit()
          sys.exit()
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
          return
  
  def new_game(self): #Setting up the actual game.

    #Creating the map
    self.map = Map(self)

    self.shell_group = pg.sprite.Group()

    #Spawning in the tanks
      #Creating the sprite groups that will be used for collisions. Creation of these groups must precede any tank object initialization, due to them being referenced in both __init__'s.
    self.player_group = pg.sprite.Group() 
    self.NPC_group = pg.sprite.Group()

      #Finding which spaces on the map are empty. An empty space is represented by a False in the map.mini_map.
    self.emptyCells = []
    for y, row in enumerate(self.map.mini_map):
      for x, cell in enumerate(row):
        if self.map.mini_map[y][x] == False:
          if  0 < x < 16 and 0 < y < 9: #For whatever reason, a bunch of negative numbers are being generated which is throwing this whole thing off. I'm just going to strong arm it.
            self.emptyCells.append((x, y)) #You have to add one to the indexed values, as on display the shown cells start at (1,1) rather than (0,0). J and I are also flipped, as indexing the mini_map uses (y, x) which must be flipped back to (x, y) for the pygame coordinate system. It took me far too long to figure that out.
    random.shuffle(self.emptyCells) #Introduce randomness to spawning. Otherwise, they would spawn in order.

      #Spawning in the two players, using the newly found free spaces.
    self.p1 = Player(self, self.emptyCells.pop(0), p1Inputs)
    self.p2 = Player(self, self.emptyCells.pop(0), p2Inputs)
      #Spawning in the NPCs
    for i in range(10):
      NPC(self, self.emptyCells.pop(0))

    self.debug = DebuggingDisplay.DebugDisplay(self)

    mixer.music.load(bg_music_path)
    mixer.music.set_volume(.25)

  def update(self):

    for player in self.player_group:
      player.update()

    for NPC in self.NPC_group:
      NPC.update()
    
    self.debug.update()

    pg.display.flip()
    self.delta_time = self.clock.tick(fps) / 1000
    pg.display.set_caption(f'COVERT COMBAT {self.clock.get_fps() :.1f}')
    
  def draw(self):
    self.screen.blit(self.bg_image, self.bg_rect)
    
    self.map.draw()
    self.p1.draw()
    self.p2.draw()
    
    for NPC in self.NPC_group:
      NPC.draw()
    
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
    self.start_menu()
    self.new_game()

    while True:
      self.check_events()
      self.update()
      self.draw()
  
  
if __name__ == '__main__':
  game = Game()
  game.run()
  