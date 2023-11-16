import pygame as pg
from settings import *
from map import *
from player import *

#A way to display object's information on the screen during runtime. 
class DebugDisplay: 
    def __init__(self, game):
        self.game = game
        self.font = pg.font.Font(None, 15)

    def update(self):
        self.watch = { #Any value you want tracked, add it here.
            'deltaTime' : self.game.delta_time,
            'TankVelocity' : self.game.p1.speed,
            'TankCoordinates' : self.game.p1.display_pos,
            'TankAngle' : self.game.p1.angle,
            'collisions' : pg.sprite.spritecollide(self.game.p1, self.game.map.walls, False),
            'maskLength' : self.game.p1.mask,
            'NPC Group' : self.game.NPC_group

        }

    def draw(self):
        yaddition = 0 #The amount of y added to the text's rectangle, to stack the text vertically down the screen
        for key in self.watch:
            displayStr = key + ': ' + str(self.watch[key])
            self.text = self.font.render(displayStr, True,(255,255,255))
            textrect = self.text.get_rect()
            textrect.centery = textrect.centery + yaddition
            self.game.screen.blit(self.text, textrect)

            yaddition += 15 #So the next line is written over the previous.


