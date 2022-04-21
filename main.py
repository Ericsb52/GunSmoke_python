# Eric Broadbent
# 4-22
# Tile map template


# imports section
import pygame as pg
from settings import *
from game import *

# creating the function to run the game
def main():
    # create the game object
    game = Game()
    # start game in title screen
    game.title_screen()
    while game.running:
        # start a new game
        game.new()
        # when player pies show game over screen
        game.gameOver_screen()

    # if player quits end game
    pg.quit()

# starts the Game

main()