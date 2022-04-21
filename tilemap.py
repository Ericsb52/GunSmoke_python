# Eric Broadbent
# Tile mad Class file
# this file has all tile map classes for the game
# 4/22


# imports
from settings import *
from player import *
from wall import *
from os import path
import pygame as pg
import pytmx

def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

class Map:
    def __init__(self,game,filename):
        self.game = game
        self.data = []
        with open(filename, "rt") as f:
            for line in f:
                self.data.append(line.strip())

        self.tileWidth = len(self.data[0])
        self.tileHeight = len(self.data)
        self.width = self.tileWidth * TILESIZE
        self.height = self.tileHeight * TILESIZE

class TiledMap:
    def __init__(self,game,filename):
        self.game = game
        tm = pytmx.load_pygame(filename,pixelalph=True)
        self.width = tm.width*tm.tilewidth
        self.height = tm.height*tm.tileheight
        self.tmxdata = tm

    def render(self,surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer,pytmx.TiledTileLayer):
                for x,y,gid in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile,(x*self.tmxdata.tilewidth,y*self.tmxdata.tileheight))
    def make_map(self):
        temp_surf = pg.Surface((self.width,self.height))
        self.render(temp_surf)
        return temp_surf


class Camera:
    def __init__(self,w,h):
        self.camera = pg.Rect(0,0,w,h)
        self.width = w
        self.height = h

    def apply(self,entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self,rect):
        return rect.move(self.camera.topleft)

    def update(self,target):
        x = -target.x +int(W_WIDTH /2)
        y = -target.y + int(W_HEIGHT /2)


        # limit scrolling of cam to the bounds of the map
        x = min(0,x)# left bounds
        y = min(0,y)# top bounds
        x = max(-(self.width - W_WIDTH),x)# right bounds
        y = max(-(self.height - W_HEIGHT),y)# bottom bounds

        self.camera = pg.Rect(x,y,self.width,self.height)

class CamTarget(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        super(CamTarget, self).__init__()
        self.image = pg.Surface((1,1))
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.vx = 0
        self.vy = CAMERA_SPEED
        self.game = game
        self.game.all_sprites.add(self)
        self.x = x
        self.y = y
        self.pos = vec(x, y)
        self.rect.center = self.pos

    def update(self):
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.rect.y = self.y