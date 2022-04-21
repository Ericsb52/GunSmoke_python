# Eric Broadbent
# walls File
# this file has all classes the the walls in the game
# 4/22


# imoprts
from settings import *

class Wall(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game = game
        self.groups = self.game.all_sprites, self.game.walls_group
        super(Wall, self).__init__(self.groups)
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Wall_tm(pg.sprite.Sprite):
    def __init__(self,game,x,y,w,h):
        self.game = game
        self.groups = self.game.walls_group
        super(Wall_tm, self).__init__(self.groups)
        self.rect = pg.Rect(x,y,w,h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y