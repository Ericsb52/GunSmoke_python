# Eric Broadbent
# Game file
# this file has all Game related Classes
# 4/6/22


# imports section
from settings import *
from player import *
from wall import *
from enemy import *
from os import path
from tilemap import *
from common_functions import *

import pygame as pg

class Game():
    def __init__(self):
        """builds game object"""
        pg.init() # setup pygame
        pg.mixer.init() #set up sound
        self.screen = pg.display.set_mode((W_WIDTH,W_HEIGHT)) #create screen
        pg.display.set_caption(TITLE) #set title
        self.clock = pg.time.Clock() #create clock
        self.running = True #game sentrie variable

    def load_data(self):
        self.game_folder = path.dirname(__file__)
        map_file = path.join(self.game_folder,"maps")
        tiled_map_file = path.join(map_file,"tiled maps")
        img_file = path.join(self.game_folder,"imgs")
        player_img_file = path.join(img_file,"player")
        enemy_img_file = path.join(img_file,"enemy")
        effects_file = path.join(img_file,"effects")
        items_file = path.join(img_file,"items")

        self.map = TiledMap(self,path.join(tiled_map_file,"Level1.tmx"))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

        self.player_walking_forward = []
        for i in range(len(PLAYER_WALKING)):
            img = pg.image.load(path.join(player_img_file,PLAYER_WALKING[i])).convert()
            img.set_colorkey(BLACK)
            self.player_walking_forward.append(img)
        self.player_walking_right = []
        for i in range(len(PLAYER_WALKING)):
            img = pg.image.load(path.join(player_img_file, PLAYER_WALKING_RIGHT[i])).convert()
            img.set_colorkey(BLACK)
            self.player_walking_right.append(img)
        self.player_walking_left = []
        for i in range(len(PLAYER_WALKING)):
            img =pg.image.load(path.join(player_img_file, PLAYER_WALKING_LEFT[i])).convert()
            img.set_colorkey(BLACK)
            self.player_walking_left.append(img)
        self.mob_img = pg.image.load(path.join(enemy_img_file,MOB_IMG)).convert()
        self.mob_img.set_colorkey(BLACK)
        self.mob_img = pg.transform.scale(self.mob_img,(TILESIZE*2,TILESIZE*2))

        self.flashes = []
        for flash in MUZZEL_FLASHES:
            self.flashes.append(pg.image.load(path.join(effects_file,flash)).convert_alpha())
        self.tumble_weed = pg.image.load(path.join(items_file,"Tumbleweeds.png"))
        self.barrel_img = pg.image.load(path.join(items_file,"barrel_img.png"))

        self.window_enemy_R = []
        for img in WINDOW_ENEMY_IMG_R:
            self.window_enemy_R.append(pg.image.load(path.join(enemy_img_file, img)).convert_alpha())
        self.window_enemy_L = []
        for img in WINDOW_ENEMY_IMG_L:
            self.window_enemy_L.append(pg.image.load(path.join(enemy_img_file, img)).convert_alpha())


    def load_music(self):
        # setup sound folders
        sound_file = path.join(self.game_folder,"sound")
        music_folder = path.join(sound_file,"music")
        ambiant_folder = path.join(sound_file,"ambiant")
        fx_folder = path.join(sound_file,"fx")
        # load game music
        self.start_music = pg.mixer.music.load(path.join(music_folder, "lassolady.ogg"))
        self.level1_music = pg.mixer.music.load(path.join(music_folder,"Western.ogg"))
        pg.mixer.music.set_volume(.5)

        # load sound fx
        self.shoot_snd_pistole = pg.mixer.Sound(path.join(fx_folder,"gunshot_pistole.wav"))
        self.shoot_snd_rifle = pg.mixer.Sound(path.join(fx_folder, "gunshot_rifle.wav"))
        self.walking_spurs = pg.mixer.Sound(path.join(fx_folder,"walking_spurs_short.wav"))


    def new(self):
        """starts new game"""
        # create groups
        self.all_sprites = pg.sprite.Group()
        self.player_group = pg.sprite.Group()
        self.walls_group = pg.sprite.Group()
        self.enemy_group = pg.sprite.Group()
        self.player_bullet_group = pg.sprite.Group()
        self.enemy_bullet_group = pg.sprite.Group()
        self.distructable_group = pg.sprite.Group()
        # load game Data
        self.load_data()
        self.load_music()



        # reading data from the map file to create objects


        # for row, tiles in enumerate(self.map.data):
        #     for col, tile in enumerate(tiles):
        #         if tile == "1":
        #             Wall(self,col,row)
        #         if tile == "t":
        #             self.target = CamTarget(self,col, row)
        #         if tile == "m":
        #             self.enemy = Enemy_Normal(self,col, row)
        #         if tile == "p":
        #             self.player = Player(self,col, row)
        for tile_obj in self.map.tmxdata.objects:
            if tile_obj.name == "player":
                self.player = Player(self, tile_obj.x, tile_obj.y)
            if tile_obj.name == "target":
                self.target = CamTarget(self, tile_obj.x, tile_obj.y)
            if tile_obj.name == "wall":
                Wall_tm(self,tile_obj.x,tile_obj.y,tile_obj.width,tile_obj.height)
            if tile_obj.name == "Enemy_one":
                Enemy_Normal(self,tile_obj.x,tile_obj.y)
            if tile_obj.name == "Window_Enemy":
                Enemy_Window(self,tile_obj.x,tile_obj.y)
            if tile_obj.name =="Weed":
                Tumble_Weed(self,vec(tile_obj.x,tile_obj.y))
            if tile_obj.name =="Barrel":
                Barrel(self,vec(tile_obj.x,tile_obj.y))






        # create the Camera
        self.camera = Camera(self.map.width,self.map.height)
        self.draw_debug = False



        self.run()

    def run(self):
        """Main Game loop runs every frame of the game"""
        # Game Loop Starts
        pg.mixer.music.play(-1)
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        """Event function gets ran in the game loop every tick
        it checks for new events and processes those events"""
        # game loop event check
        for event in pg.event.get():
            # check for window closing
            if event.type ==pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug

        # Cheking for Colisions
        # player bullets hiting enemys
        hits = pg.sprite.groupcollide(self.enemy_group,self.player_bullet_group,False,True)
        for hit in hits:
            hit.take_dmg(BULLET_DMG)
        # enemy bullets hitting player
        hits = pg.sprite.spritecollide(self.player,self.enemy_bullet_group,True)
        for hit in hits:
            self.player.take_dmg(hit.damage)
        # enemy hitting player
        hits = pg.sprite.spritecollide(self.player,self.enemy_group,False)
        for hit in hits:
            self.player.take_dmg(hit.damage)
            hit.vel = vec(0,0)
            if self.player.health <= 0:
                self.playing = False
        if hits:
            self.player.pos += vec(MOB_KNOCKBACK,0).rotate(-hits[0].rot)
        hits = pg.sprite.groupcollide(self.distructable_group,self.player_bullet_group,False,True)
        for hit in hits:
            hit.take_dmg(BULLET_DMG)



    def update(self):
        """Update function gets called every tick
        and it will update all sprites in the game """
        # game loop update
        self.all_sprites.update()
        self.camera.update(self.target)
    def draw_grid(self):
        for x in range(0,W_WIDTH,TILESIZE):
            pg.draw.line(self.screen,WHITE,(x,0),(x,W_HEIGHT))
        for y in range(0,W_HEIGHT,TILESIZE):
            pg.draw.line(self.screen,WHITE,(0,y),(W_WIDTH,y))


    def draw(self):
        """Draw function gets called every tick
        it will draw the sprites at their new updated locations"""
        # game loop draw
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps())) # for debugging and testing
        # self.screen.fill(BROWN)
        # self.draw_grid()
        self.screen.blit(self.map_img,self.camera.apply_rect(self.map_rect))

        for sprite in self.all_sprites:
            # if isinstance(sprite,Enemy_Normal):
            #     sprite.draw_health()
            self.screen.blit(sprite.image,self.camera.apply(sprite))
            if self.draw_debug:
                pg.draw.rect(self.screen,GREEN,self.camera.apply_rect(sprite.hit_rect),1)
        if self.draw_debug:
            for wall in self.walls_group:
                pg.draw.rect(self.screen, GREEN, self.camera.apply_rect(wall.rect),1)

        # hud Section
        draw_player_health(self.screen, 32, 16, self.player.health / PLAYER_HEALTH)



        pg.display.flip()

    def title_screen(self):
        """Title Screen"""
        pass

    def gameOver_screen(self):
        """Game Over screen"""
        pass