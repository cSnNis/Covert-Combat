import pygame as pg

#Display settings
res = WIDTH,HEIGHT = 800,400
fps = 60 

#Tank Settings
    #Starting position values
player_pos = 2,5

player_pos = 1.5,5
player_angle = 0 #in radians
    #Movement settings
player_accel = 1
player_deceleration = .8 #The rate at which velocity is lost after a player stops pressing. This value is multiplied by velocity, so a value of .5 would halve the velocity per second.
x_change = 0
y_change = 0
accelsens = .1 #How low x or y acceleration can go before it rounds to zero. This MUST be greater than the player_accel.
player_max_speed = 3

    #Collision Settings
bounceSpeedFactor = 1.1 #How much more energy the tank bounces off the wall with.
minimumBounceSpeed = 1 #The minimum velocity of bounce from a collision. This is for when tanks rotate into a collision, rather than drive into a collision. 
bounceDeceleration = 1 #The rate at which the bounce loses velocity.

    
    #Tank Sprites
tank_sprite_path = 'TankBody.png'
turret_sprite_path = 'Turret.png'
tank_scale = .5 #Scaling the dimensions for the tanks.
tankSpriteScalingFactor = 1

player_rot_speed = 1 #Radians per second
turret_rot_speed = 2

    #Player inputs, as tuples
    #The order is (forwardKey, backwardKey, leftKey, rightKey, turretLeftKey, turretRightKey)
p1Inputs = (pg.K_w, pg.K_s, pg.K_a, pg.K_d, pg.K_q, pg.K_e)
p2Inputs = (pg.K_UP, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT, pg.K_PERIOD, pg.K_SLASH)

#Tile Settings
tile_sprite_path = 'wall image.jpg'



# DO NOT CHANGE VALUES BELOW THIS LINE unless you're sure. They are calculated based off of earlier set values.
# They are not safe to change, as changing them could set off proportions. 

#Screen dimension multipliers. Multiply anything displayed by these to correct for changed resolution.
RESMULTX = res[0] / 1600 
RESMULTY = res[1] / 900

COORDINATEMULT = COORDINATEMULTX, COORDINATEMULTY =  100 * RESMULTX, 100 * RESMULTY
