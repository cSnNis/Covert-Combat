"""
This function is meant for pg.sprite.Sprite objects to use. It returns a tuple, which;
    The first element is a boolean if the collision occurred
    The second is a reference to the object it occured in
    The third is the location of the collision in display coordinates.

You also need to add a self.collidables list in the __init__(). This will contain what groups of sprites this sprite should check for collisions against. In player.py, this looks like

self.collidables = [self.game.map.walls]

To help visualize the collisions and aid any debugging, this function, by default, also draws a rectangle where the collision happens, and also draws the mask at the top right corner when it happens.
Just remove the lines at 27, 28 and 34 if you want them gone.

"""


def checkCollision(self): #Detects for pixel-based collisions between this sprite and anything in group self.collidables, returns the name of the collided object and it's point in display space.
        for group in self.collidables: 
            collisions = pg.sprite.spritecollide(self, group, False)
            if len(collisions) > 0: #If there exists a collision, 
                collision = collisions[0] #Only calculate the first object of this group.
                
                maskCollisionPoint = pg.sprite.collide_mask(self, collision) #The x and y coordinate of the collision, in the local space of the mask's rectangle (top corner of the rectangle is 0,0)
                if maskCollisionPoint == None:
                    return False, None, (0,0) #If collide_mask returns None, then there is no collision to calculate.

                self.game.screen.set_at(maskCollisionPoint, 'blue')
                self.game.screen.blit(self.mask.to_surface(), self.mask.get_rect())

                #Find that intersecting point in world game space.
                x = self.rect.left + maskCollisionPoint[0] #Calculating the local space coordinate transposed onto world space. self.rect is the rectangle for the tank sprite.
                y = self.rect.top + maskCollisionPoint[1]

                pg.draw.rect(self.game.screen, 'blue', pg.Rect(x, y, 5,5)) #Helper function to draw where that collision was.

                return True, collision, (x,y)
            return False, None, (0,0) #If there are no objects colliding, then return False also.
