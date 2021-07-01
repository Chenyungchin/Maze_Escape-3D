
import pygame
from game import Game

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 576

FPS = 60

def main():
    
    pygame.init()
    
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    
    pygame.display.set_caption("Maze Escape-3D")
    
    done = False
    
    clock = pygame.time.Clock()
    
    game = Game()
   
    while not done:
        done = game.process_events()
        game.display_frame(screen)
        clock.tick(FPS)
    pygame.quit()

if __name__ == '__main__':
    main()
