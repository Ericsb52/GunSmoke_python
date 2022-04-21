# Eric Broadbent
# Player File
# this file has all classes the the player will use
# 4/6/22

# imports section
import pygame as pg
from settings import *
from bullets import *
from extras import *
from common_functions import *
vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        super(Player, self).__init__()
        self.game = game
        # self.image = pg.Surface((TILESIZE,TILESIZE))
        # self.image.fill(YELLOW)
        # image propertys
        self.image = self.game.player_walking_forward[0]
        self.image = pg.transform.scale(self.image,(TILESIZE*2,TILESIZE*2))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center

        # movment propertys

        self.pos = vec(x,y)
        self.vel = vec(0,0)
        self.acc = vec(0,0)

        # shooting properties
        self.shoot_delay = 400
        self.last_shot = pg.time.get_ticks()
        self.rect.center = self.pos

        # add player to groups
        self.game.all_sprites.add(self)
        self.game.player_group.add(self)

        # animation propertys
        self.animation_frame = 0
        self.frame_rate = 300
        self.last_animate = pg.time.get_ticks()

        # walking sound propertys
        self.last_sound = pg.time.get_ticks()
        self.sound_time = 400

        # health propertys
        self.health = PLAYER_HEALTH

    def take_dmg(self, dmg):
        self.health -= dmg

    def die(self):
        self.kill()

    def animate(self):
        if self.vel.y and not self.vel.x:
            now = pg.time.get_ticks()
            if now - self.last_animate > self.frame_rate:
                self.animation_frame += 1
                if self.animation_frame > len(self.game.player_walking_forward)-2:
                    self.animation_frame = 0
                self.last_animate = now
                old_rect = self.rect.center
                image = self.game.player_walking_forward[self.animation_frame]
                self.image = image
                self.image = pg.transform.scale(self.image,(TILESIZE*2,TILESIZE*2))
                self.image.set_colorkey(BLACK)
                self.rect = self.image.get_rect()
                self.rect.center = old_rect
                if now - self.last_sound > self.sound_time:
                    self.last_sound = now
                    self.game.walking_spurs.play()

        elif self.vel.x < 0:
            now = pg.time.get_ticks()
            if now - self.last_animate > self.frame_rate:
                self.animation_frame += 1
                if self.animation_frame > len(self.game.player_walking_left) - 2:
                    self.animation_frame = 0
                self.last_animate = now
                old_rect = self.rect.center
                image = self.game.player_walking_left[self.animation_frame]
                self.image = image
                self.image = pg.transform.scale(self.image,(TILESIZE*2,TILESIZE*2))
                self.image.set_colorkey(BLACK)
                self.rect = self.image.get_rect()
                self.rect.center = old_rect
                if now - self.last_sound > self.sound_time:
                    self.last_sound = now
                    self.game.walking_spurs.play()

        elif self.vel.x > 0:
            now = pg.time.get_ticks()
            if now - self.last_animate > self.frame_rate:
                self.animation_frame += 1
                if self.animation_frame > len(self.game.player_walking_right) - 2:
                    self.animation_frame = 0
                self.last_animate = now
                old_rect = self.rect.center
                image = self.game.player_walking_right[self.animation_frame]
                self.image = image
                self.image = pg.transform.scale(self.image,(TILESIZE*2,TILESIZE*2))
                self.image.set_colorkey(BLACK)
                self.rect = self.image.get_rect()
                self.rect.center = old_rect
                if now - self.last_sound > self.sound_time:
                    self.last_sound = now
                    self.game.walking_spurs.play()

        else:
            self.animation_frame = 0
            now = pg.time.get_ticks()
            self.last_animate = now
            old_rect = self.rect.center
            image = self.game.player_walking_forward[0]
            self.image = image
            self.image = pg.transform.scale(self.image, (TILESIZE*2,TILESIZE*2))
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.center = old_rect
            self.game.walking_spurs.stop()




    def get_keys(self):
        self.vel = vec(0,0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y = -PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y = PLAYER_SPEED
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071


        # shoot keys
        if keys[pg.K_m] and keys[pg.K_n]:
            self.shoot_str()
        elif keys[pg.K_m]:
            self.shoot_right()
        elif keys[pg.K_n]:
            self.shoot_left()
    # no longer used
    def colide_with_walls(self,dir):
        if dir == "x":
            hits = pg.sprite.spritecollide(self,self.game.walls_group,False,)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == "y":
            hits = pg.sprite.spritecollide(self,self.game.walls_group,False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y

    def update(self):

        self.animate()
        self.get_keys()



        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        now = pg.time.get_ticks()

        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls_group, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls_group, 'y')
        self.rect.center = self.hit_rect.center

        if self.health <= 0:
            self.die()

    def shoot_left(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            self.game.shoot_snd_pistole.play()
            Bullet(self.game,vec(-10,-15),(self.rect.left,self.rect.top - 3))
            Bullet(self.game, vec(-8, -15), (self.rect.right, self.rect.top - 3))
            MuzzelFlash(self.game,(self.rect.left,self.rect.top - 3))
            MuzzelFlash(self.game, (self.rect.right, self.rect.top - 3))


    def shoot_str(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            self.game.shoot_snd_pistole.play()
            Bullet(self.game,vec(0,-15),(self.rect.left,self.rect.top - 3))
            Bullet(self.game, vec(0, -15), (self.rect.right, self.rect.top - 3))
            MuzzelFlash(self.game, (self.rect.left, self.rect.top - 3))
            MuzzelFlash(self.game, (self.rect.right, self.rect.top - 3))

    def shoot_right(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            self.game.shoot_snd_pistole.play()
            Bullet(self.game, vec(8, -15), (self.rect.left, self.rect.top - 3))
            Bullet(self.game, vec(10, -15), (self.rect.right, self.rect.top - 3))
            MuzzelFlash(self.game, (self.rect.left, self.rect.top - 3))
            MuzzelFlash(self.game, (self.rect.right, self.rect.top - 3))



