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
      pg.display.set_caption(f'COVERT COMBAT {self.clock.get_fps() :.1f}')
      for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
          pg.quit()
          sys.exit()
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
          return

  def victory_screen(self):
    #Play the victory music.
    self.bg_music.load(victory_music_path)
    self.bg_music.set_volume(.25)
    self.bg_music.play()

    #Determine who won.
    if self.player_group.sprites()[0].inputs == p1Inputs: #If it's player 1;
      winner = 'Player 1'
      loser = 'Player 2'
    else:
      winner = 'Player 2'
      loser = 'Player 1'
    #Generate the appropriate victory text.
    victory_text = pg.font.Font(start_font_path,45).render((winner + " found and destroyed " + loser + ". Press Space to Play Again."), None, 'white', 'black'); victory_text = pg.transform.scale(victory_text, (victory_text.get_width() * RESMULTX, victory_text.get_height() * RESMULTY))
    victory_text_rect = victory_text.get_rect(center = (res[0] / 2, res[1] / 2))

    #Display this text while waiting for a player to start a new game.
    while True: #Wait until a key is pressed to exit. 
      pg.display.set_caption(f'COVERT COMBAT {self.clock.get_fps() :.1f}')
      self.draw()
      self.screen.blit(victory_text, victory_text_rect)
      pg.display.flip()
      for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
          pg.quit()
          sys.exit()
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
          return

  def new_game(self): #Setting up the actual game.

    #Creating the map
    self.map = Map(self)

    self.obs_group = pg.sprite.Group() #obstacles

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
    mixer.music.set_volume(bg_music_volume)
    mixer.music.play(-1)

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

    for player in self.player_group:
      player.draw()


    if pg.key.get_pressed()[pg.K_1]:
      pg.draw.circle(self.screen, 'BLUE', self.p1.display_pos, int(player_intel_diameter*RESMULTX), width=int(player_intel_width*RESMULTX))
    if pg.key.get_pressed()[pg.K_2]:
      pg.draw.circle(self.screen, 'GREEN', self.p2.display_pos, int(player_intel_diameter*RESMULTX), width=int(player_intel_width*RESMULTX))
    
    for NPC in self.NPC_group:
      NPC.draw()
    
    self.obs_group.draw(self.screen)
    self.debug.draw()



  def check_events(self):
    for event in pg.event.get():
      if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
        pg.quit()
        sys.exit()
        
        
    
  def run(self):
    self.start_menu()
    while True: #Keep looping until the game quits.
      self.new_game()

      while len(self.player_group) > 1: #While there exist two players
        self.check_events()
        self.update()
        self.draw()

      self.victory_screen()
  
  
if __name__ == '__main__':
  game = Game()
  game.run()
  