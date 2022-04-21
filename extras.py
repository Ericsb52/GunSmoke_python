# Eric Broadbent
# Extras file contains classes for power ups distructables and enviroment details
# this file has all tile map classes for the game
# 4/22

# imports
from settings import *
from os import path
import pygame as pg
import random


class Barrel(pg.sprite.Sprite):
    def __init__(self,game,pos):
        self.game = game
        self.groups = self.game.all_sprites,self.game.distructable_group
        super(Barrel, self).__init__(self.groups)
        self.image = self.game.barrel_img
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = self.pos
        self.health = 50

    def update(self):
        if self.health <= 0:
            self.destroy()

    def take_dmg(self,dmg):
        self.health -= dmg


    def destroy(self):
        pos = self.pos
        self.kill()
        num = random.randint(1,100)
        if num > 90:
            self.spawn_power_up()

    def spawn_power_up(self):
        print("spawn powerup")



class Power_Up(pg.sprite.Sprite):
    pass


class Tumble_Weed(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self.groups = game.all_sprites,game.distructable_group
        super(Tumble_Weed, self).__init__(self.groups)
        self.game = game
        self.size = random.randint(16, 32)
        self.image_orig = pg.transform.scale(self.game.tumble_weed, (self.size, self.size))
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.rot = 0
        self.rotspeed = random.randint(5,10)
        self.pos = pos
        self.speed = 5
        self.rect.center = pos
        self.spawntime = pg.time.get_ticks()
        self.lifetime = 5000
        self.last_animate = pg.time.get_ticks()
        self.frame_rate = 50
        if self.pos.x < W_WIDTH /2:
            self.rotspeed *= -1
        else:
            self.speed *= -1

    def update(self):
        self.animate()
        self.rect.centerx += self.speed
        now = pg.time.get_ticks()
        if now - self.spawntime > self.lifetime:
            self.kill()

    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_animate > self.frame_rate:
            self.last_animate = now
            self.rot = (self.rot + self.rotspeed)%360
            new_image = pg.transform.rotate(self.image_orig,self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

class MuzzelFlash(pg.sprite.Sprite):
    def __init__(self,game,pos):
        self.groups = game.all_sprites
        super(MuzzelFlash, self).__init__(self.groups)
        self.game = game
        self.size = random.randint(10,16)
        self.image = pg.transform.scale(random.choice(game.flashes),(self.size,self.size))
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.spawntime = pg.time.get_ticks()

    def update(self):
        if pg.time.get_ticks() - self.spawntime > FLASH_DUR:
            self.kill()