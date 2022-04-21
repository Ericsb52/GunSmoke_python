# Eric Broadbent
# enemy File
# this file has all classes the the enemy will use
# 4/6/22


# imports section
import pygame as pg
from settings import *
from bullets import *
from common_functions import *
vec = pg.math.Vector2

class Enemy_Normal(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        super(Enemy_Normal, self).__init__()
        self.game = game

        # self.image = pg.Surface((TILESIZE*2,TILESIZE*2))
        # self.image.fill(RED)
        self.image = self.game.mob_img.copy()
        self.rect = self.image.get_rect()

        self.hit_rect = MOB_HIT_RECT
        self.hit_rect.center = self.rect.center


        self.pos = vec(x,y)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.rect.center = self.pos
        self.rot = 0
        self.health = 100

        self.damage = MOB_DMG

        self.game.all_sprites.add(self)
        self.game.enemy_group.add(self)

    # no longer used
    def colide_with_walls(self,dir):
        if dir == "x":
            hits = pg.sprite.spritecollide(self,self.game.walls_group,False)
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

    def avoid_mobs(self):
        for mob in self.game.enemy_group:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < AVOID_RADIUS:
                    self.acc += dist.normalize()

    def update(self):
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1,0))
        self.acc = vec(MOB_SPEED,0).rotate(-self.rot)
        self.avoid_mobs()
        self.acc.scale_to_length(MOB_SPEED)
        self.acc += self.vel *-1
        self.vel += self.acc*self.game.dt
        self.pos += self.vel * self.game.dt+0.5*self.acc*self.game.dt**2
        self.rect.center = self.pos

        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls_group, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls_group, 'y')
        self.rect.center = self.hit_rect.center



        if self.health <= 0:
            self.kill()
        num = random.randint(1,100)
        if num > 99:
            self.shoot_at()


    def take_dmg(self, dmg):
        self.vel = vec(0,0)
        self.health -= dmg


    def draw_health(self):
        if self.health > 60:
            col = GREEN
        elif self.health > 30:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / MOB_HEALTH)
        self.health_bar = pg.Rect(0, 0, width, 7)
        if self.health < MOB_HEALTH:
            pg.draw.rect(self.image, col, self.health_bar)


    def shoot_at(self):
        print("shooting at player")
        target_x = self.game.player.rect.centerx
        target_y = self.game.player.rect.centery
        angle = math.atan2(target_y-self.rect.centery,target_x-self.rect.centerx)
        self.dx = math.cos(angle)
        self.dy = math.sin(angle)
        dir = vec(self.dx,self.dy)
        b = Enemy_bullet(self.game,self.rect.center,dir)




# boss fight update
# self.rot = (self.game.player.pos - self.pos).angle_to(vec(1,0))
# self.acc = vec(MOB_SPEED,0).rotate(-self.rot)
# self.acc += self.vel *-1
# self.vel += self.acc*self.game.dt
# self.pos += self.vel * self.game.dt+0.5*self.acc*self.game.dt**2
# self.rect.center = self.pos