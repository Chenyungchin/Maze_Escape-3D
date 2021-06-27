import sys, time
import random
import pygame
from pygame.locals import Color, QUIT, MOUSEBUTTONDOWN, USEREVENT, USEREVENT

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
IMAGEWIDTH = 300
IMAGEHEIGHT = 200
FPS = 60

white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
orange = (255, 165, 0)
blue_violet = (138, 43, 226)
cyan = (0, 255, 255)
lightcoral = (240, 128, 128)

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Maze Escape-3D")
clock = pygame.time.Clock()

x = 40
y = 30
grid = []

# build the grid
def build_grid(width, height):
    w = 720//width
    x = 40
    y = 30
    for i in range(height):
        for j in range(width):
            pygame.draw.line(screen, white, (x, y), (x + w, y))
            pygame.draw.line(screen, white, (x + w, y), (x + w, y + w))
            pygame.draw.line(screen, white, (x + w, y + w), (x, y + w))
            pygame.draw.line(screen, white, (x, y + w), (x, y))
            grid.append((x,y))
            x = x + w
        x = 40
        y += w
    
    pygame.display.update()

def remove_horizontal(x, y, w):
    pygame.draw.line(screen, black, (x, y), (x + w, y))
    pygame.display.update()

def remove_vertical(x, y, w):
    pygame.draw.line(screen, black, (x, y), (x, y + w))
    pygame.display.update()

difficulty = "hard"

if difficulty == "easy":
    build_grid(12, 9)
    w = 720 // 12
elif difficulty == "normal":
    build_grid(16, 12)
    w = 720 // 16
elif difficulty == "hard":
    build_grid(20, 15)
    w = 720 // 20

# remove_horizontal(40+4*w, 30+8*w, w)
# remove_vertical(40+3*w, 30+w, w)

run = True
while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        # check for closing the window
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

