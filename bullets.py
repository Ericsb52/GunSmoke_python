# Eric Broadbent
# progectiles file
# file has all classes the have to do with projectiles
# 4/6/22


# imports section
import pygame as pg
from settings import *
import math
vec = pg.math.Vector2



class Bullet(pg.sprite.Sprite):
    def __init__(self,game,speed_vec,center):
        super(Bullet, self).__init__()
        self.game = game
        self.image = pg.Surface((5,5))
        self.image.fill(BLACK)
        self.rect =self.image.get_rect()
        self.hit_rect = self.rect
        self.rect.center = center
        self.speed = vec(speed_vec)
        self.game.all_sprites.add(self)
        self.game.player_bullet_group.add(self)
        self.lifetime = 20
        self.damage = BULLET_DMG


    def update(self):
        self.rect.center += self.speed
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()




class Enemy_bullet(pg.sprite.Sprite):
    def __init__(self,game,pos,dir):
        super(Enemy_bullet, self).__init__()
        self.game = game
        self.bullet_speed = 600
        self.game.all_sprites.add(self)
        self.game.enemy_bullet_group.add(self)
        self.image = pg.Surface((5, 5))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = pos
        self.rect.center = pos
        self.vel = dir * self.bullet_speed
        self.life_time = 1500
        self.spawn_time = pg.time.get_ticks()
        self.damage = BULLET_DMG


    def update(self):
        self.pos += self.vel*self.game.dt
        self.rect.center = self.pos

        if pg.time.get_ticks() - self.spawn_time > self.life_time:
            self.kill()



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