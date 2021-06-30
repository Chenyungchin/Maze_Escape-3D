#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from game import Game

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 576

FPS = 60

def main():
    # Initialize all imported pygame modules
    pygame.init()
    # Set the width and height of the screen [width, height]
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    # Set the current window caption
    pygame.display.set_caption("Maze Escape-3D")
    #Loop until the user clicks the close button.
    done = False
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    # Create a game object
    game = Game()
    # -------- Main Program Loop -----------
    while not done:
        done = game.process_events()
        game.display_frame(screen)
        clock.tick(FPS)
    pygame.quit()

if __name__ == '__main__':
    main()
