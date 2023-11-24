import pygame as pg


#Display settings
res = WIDTH,HEIGHT = 800,450
fps = 60 

#Start Menu settings
splash_image_path = "MenuResources/CovertCombatSplashArt.png"
logo_image_path = "MenuResources/CovertCombatLogo.png"
start_instructions = ["You and the other player control two tanks hidden amongst a sea of tanks.",
                       "It is your job to hunt and kill the other player, without being killed.",
                       "To find your tank, press 1 for P1 and 2 for P2 to reveal them. Be careful not to reveal yourself.",
                       "Press SPACE to start, or ESC to quit."]
start_music_path = 'TankMusicSounds/05 - Theme 2.mp3'
start_font_path = 'MenuResources/Capsmall.ttf'

#Victory Screen Settings
victory_music_path = 'TankMusicSounds/02 - Briefing.mp3'

#Background music settings
bg_music_volume = .15
bg_music_path = 'TankMusicSounds\BattleMusic.mp3'

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
bounceSpeedFactor = 1.1 #How much more energy the tank bounces off the wall with.
minimumBounceSpeed = 1 #The minimum velocity of bounce from a collision. This is for when tanks rotate into a collision, rather than drive into a collision. 
bounceDeceleration = 1 #The rate at which the bounce loses velocity.

    #Tank Sprites
tank_sprite_path = 'images/tank/GreenTankBody.png'
turret_sprite_path = 'images/tank/Turret.png'
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
shell_sprite_path = 'images/tank/Shell.png'
shell_sprite_dimensions = (50,50)

    #Player inputs, as tuples
    #The order is (forwardKey, backwardKey, leftKey, rightKey, turretLeftKey, turretRightKey, fireButton)
p1Inputs = (pg.K_w, pg.K_s, pg.K_a, pg.K_d, pg.K_c, pg.K_v, pg.K_LSHIFT)
p2Inputs = (pg.K_UP, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT, pg.K_PERIOD, pg.K_SLASH, pg.K_RSHIFT)

    #Tank Sounds
turret_rot_volume = .35
turret_rot_sound_path = 'TankMusicSounds\TurretRotate.mp3'
wall_thud_volume = .75
wall_thud_sound_path = 'TankMusicSounds\WallThud.mp3'
engine_sound_path = 'TankMusicSounds\EngineSound.mp3'
tank_shoot_path = 'TankMusicSounds\TankShoot.mp3'
tank_shoot_volume = .12
tank_explosion_path = 'TankMusicSounds\TankExplosion.mp3'
tank_explosion_volume = .35

#General Sounds
fence_collision_path = 'TankMusicSounds\FenceHit.mp3'
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
GREENTANKIMAGE = pg.image.load('images/tank/GreenTankBody.png').convert_alpha(); GREENTANKIMAGE = pg.transform.scale(GREENTANKIMAGE, (GREENTANKIMAGE.get_width() * RESMULTX * tankSpriteScalingFactor, GREENTANKIMAGE.get_height() * RESMULTY * tankSpriteScalingFactor))  # Load player image, scale it by the set scaling factor and the set resolution.
GREENTURRETIMAGE = pg.image.load('images/tank/GreenTurret.png').convert_alpha(); GREENTURRETIMAGE = pg.transform.scale(GREENTURRETIMAGE, (GREENTURRETIMAGE.get_width() * RESMULTX * tankSpriteScalingFactor, GREENTURRETIMAGE.get_height() * RESMULTY * tankSpriteScalingFactor))  # Load player image, scale it by the set scaling factor and the set resolution.
#BLUETANKIMAGE
#BLUETURRETIMAGE <- Will be added later

    #List of tank sprite pairs, which BaseTank picks a random set from when it's initialized.
TANKSPRITELIST = [(GREENTANKIMAGE, GREENTURRETIMAGE)]

#Pre-loading sounds
THUDSOUND = pg.mixer.Sound(turret_rot_sound_path)


