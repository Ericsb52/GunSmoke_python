# Eric Broadbent
# settings file
# this file has all the global settings for the whole game
# 4/6/22

# imports section
import pygame as pg
import random


# window settings
W_WIDTH = 512
W_HEIGHT = 720
TITLE = "Gun Smoke"
FPS = 60

# tile settings
TILESIZE = 16
GRIDWIDTH = W_WIDTH/TILESIZE
GRIDHEIGHT = W_HEIGHT/TILESIZE

# define colors
# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)

# camera settings
CAMERA_SPEED = -35


# player settings
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_SPEED = 300
PLAYER_HEALTH = 100
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
PLAYER_WALKING = ["Main_Character_walking_1.png","Main_Character_walking_2.png",
                  "Main_Character_walking_3.png","Main_Character_walking_4.png"]
PLAYER_WALKING_RIGHT = ["Main_Character_walking_right_1.png","Main_Character_walking_right_2.png",
                  "Main_Character_walking_right_3.png","Main_Character_walking_right_4.png"]
PLAYER_WALKING_LEFT = ["Main_Character_walking_left_1.png","Main_Character_walking_left_2.png",
                  "Main_Character_walking_left_3.png","Main_Character_walking_left_4.png"]


# wall settings


# enemy settings
MOB_IMG = "Outlaws.png"
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)
MOB_SPEED = random.randint(100,150)
MOB_HEALTH = 100
MOB_DMG = 35
MOB_KNOCKBACK = 20
AVOID_RADIUS = 75
CHASE_RADIUS = 300
SHOOT_RADIUS = 150
WINDOW_SHOOT_RADIUS = 300
WINDOW_ENEMY_IMG_R = ["Outlaws_window_right1.png","Outlaws_window_right2.png","Outlaws_window_right3.png"]
WINDOW_ENEMY_IMG_L = ["Outlaws_window_left1.png","Outlaws_window_left2.png","Outlaws_window_left3.png",]
# bullet setting
BULLET_DMG = 20
MUZZEL_FLASHES = ["whitePuff15.png","whitePuff16.png","whitePuff17.png","whitePuff18.png"]
FLASH_DUR = 40



