import pygame as pg


#Display settings
res = WIDTH,HEIGHT = 800,450
fps = 60 

#Start Menu settings
splash_image_path = "MenuResources/CovertCombatSplashArt.png"
logo_image_path = "MenuResources/CovertCombatLogo.png"
start_instructions = ["You and the other player control two tanks hidden amongst a sea of tanks.",
                       "It is your job to hunt and kill the other player, without being killed.",
                       "P1: Use WASD to move, and C and V to turn the turret. LSHIFT to shoot.",
                       "P2: Use the Arrows Keys to move, and . and / to turn the turret. RSHIFT to shoot.",
                       "To find your tank, press 1 for P1 and = (EQUALS key) for P2 to reveal them to everyone.",
                        "Be careful not to reveal yourself.",
                       "Press SPACE to start, or ESC to quit."]
start_music_path = 'TankMusicSounds/05 - Theme 2.mp3'
start_font_path = 'MenuResources/Capsmall.ttf'

#Victory Screen Settings
victory_music_path = 'TankMusicSounds/02 - Briefing.mp3'

#Background music settings
bg_music_volume = .15
bg_music_path = 'TankMusicSounds/BattleMusic.mp3'

#Sets the size of the circle showing each player
player_intel_diameter = 80
player_intel_width = 8

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
minimumBounceSpeed = .09 #The minimum velocity of bounce from a collision. This is for when tanks rotate into a collision, rather than drive into a collision. It must be less than accel_sens to prevent runaway collisions into a wall.
bounceDeceleration = 1 #The rate at which the bounce loses velocity.

    #Tank Sprites
tank_scale = .5 #Scaling the dimensions for the tanks.
tankSpriteScalingFactor = 1

    #Destroyed Images
GD_path = 'images/obstacles/G_Destroyed.png'
RD_path = 'images/obstacles/R_Destroyed.png'
BD_path = 'images/obstacles/B_Destroyed.png'
Explosion_path = 'images/tank/Explosion.gif'

player_rot_speed = 1 #Radians per second
turret_rot_speed = 2

    #Shooting Settings
ShellCooldownTime = 1
shell_sprite_path = 'images/tank/Shell.png'
shell_sprite_dimensions = (50,50)

    #Player inputs, as tuples
    #The order is (forwardKey, backwardKey, leftKey, rightKey, turretLeftKey, turretRightKey, fireButton)
p1Inputs = (pg.K_w, pg.K_s, pg.K_a, pg.K_d, pg.K_c, pg.K_v, pg.K_LSHIFT)
p2Inputs = (pg.K_UP, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT, pg.K_PERIOD, pg.K_SLASH, pg.K_RSHIFT)

    #Tank Sounds
turret_rot_volume = .35
turret_rot_sound_path = 'TankMusicSounds/TurretRotate.mp3'
wall_thud_volume = .75
wall_thud_sound_path = 'TankMusicSounds/WallThud.mp3'
engine_sound_path = 'TankMusicSounds/EngineSound.mp3'
tank_shoot_path = 'TankMusicSounds/TankShoot.mp3'
tank_shoot_volume = .12
tank_explosion_path = 'TankMusicSounds/TankExplosion.mp3'
tank_explosion_volume = .35

#General Sounds
fence_collision_path = 'TankMusicSounds/FenceHit.mp3'
fence_collision_volume = .3

#Tile Settings
tile_sprite_path = 'images/obstacles/wall image.jpg'



# DO NOT CHANGE VALUES BELOW THIS LINE unless you're sure. They are calculated based off of earlier set values.
# They are not safe to change, as changing them could set off proportions. 

#These must be initialized here to preload images, as Pygame requires a resolution be set and it's image modules be initialized.
pg.init()
pg.display.set_mode(res)

#Screen dimension multipliers. Multiply anything displayed by these to correct for changed resolution.
RESMULTX = res[0] / 1600 
RESMULTY = res[1] / 900

COORDINATEMULT = COORDINATEMULTX, COORDINATEMULTY =  100 * RESMULTX, 100 * RESMULTY


#Pre-loading tank images
GREENTANKIMAGE = pg.image.load('images/tank/GreenTankBody.png').convert_alpha(); GREENTANKIMAGE = pg.transform.scale(GREENTANKIMAGE, (GREENTANKIMAGE.get_width() * RESMULTX * tankSpriteScalingFactor, GREENTANKIMAGE.get_height() * RESMULTY * tankSpriteScalingFactor))
GREENTURRETIMAGE = pg.image.load('images/tank/GreenTurret.png').convert_alpha(); GREENTURRETIMAGE = pg.transform.scale(GREENTURRETIMAGE, (GREENTURRETIMAGE.get_width() * RESMULTX * tankSpriteScalingFactor, GREENTURRETIMAGE.get_height() * RESMULTY * tankSpriteScalingFactor))
GREENDESTROYED = pg.image.load('images/obstacles/G_Destroyed.png').convert_alpha(); GREENDESTROYED = pg.transform.scale(GREENDESTROYED, (GREENDESTROYED.get_width() * RESMULTX * tankSpriteScalingFactor, GREENDESTROYED.get_height() * RESMULTY * tankSpriteScalingFactor))

BLUETANKIMAGE = pg.image.load('images/tank/BlueTankBody.png').convert_alpha(); BLUETANKIMAGE = pg.transform.scale(BLUETANKIMAGE, (BLUETANKIMAGE.get_width() * RESMULTX * tankSpriteScalingFactor, BLUETANKIMAGE.get_height() * RESMULTY * tankSpriteScalingFactor))
BLUETURRETIMAGE = pg.image.load('images/tank/BlueTurret.png').convert_alpha(); BLUETURRETIMAGE = pg.transform.scale(BLUETURRETIMAGE, (BLUETURRETIMAGE.get_width() * RESMULTX * tankSpriteScalingFactor, BLUETURRETIMAGE.get_height() * RESMULTY * tankSpriteScalingFactor))
BLUEDESTROYED = pg.image.load('images/obstacles/B_Destroyed.png').convert_alpha(); BLUEDESTROYED = pg.transform.scale(BLUEDESTROYED, (BLUEDESTROYED.get_width() * RESMULTX * tankSpriteScalingFactor, BLUEDESTROYED.get_height() * RESMULTY * tankSpriteScalingFactor))

REDTANKIMAGE = pg.image.load('images/tank/RedTankBody.png').convert_alpha(); REDTANKIMAGE = pg.transform.scale(REDTANKIMAGE, (REDTANKIMAGE.get_width() * RESMULTX * tankSpriteScalingFactor, REDTANKIMAGE.get_height() * RESMULTY * tankSpriteScalingFactor))
REDTURRETIMAGE = pg.image.load('images/tank/RedTurret.png').convert_alpha(); REDTURRETIMAGE = pg.transform.scale(REDTURRETIMAGE, (REDTURRETIMAGE.get_width() * RESMULTX * tankSpriteScalingFactor, REDTURRETIMAGE.get_height() * RESMULTY * tankSpriteScalingFactor))
REDDESTROYED = pg.image.load('images/obstacles/R_Destroyed.png').convert_alpha(); REDDESTROYED = pg.transform.scale(REDDESTROYED, (REDDESTROYED.get_width() * RESMULTX * tankSpriteScalingFactor, REDDESTROYED.get_height() * RESMULTY * tankSpriteScalingFactor))

    #List of tank sprite pairs, which BaseTank picks a random set from when it's initialized.
TANKSPRITELIST = [(GREENTANKIMAGE, GREENTURRETIMAGE, GREENDESTROYED), (BLUETANKIMAGE, BLUETURRETIMAGE, BLUEDESTROYED), (REDTANKIMAGE, REDTURRETIMAGE, REDDESTROYED)]

#Pre-loading sounds
THUDSOUND = pg.mixer.Sound(turret_rot_sound_path)


