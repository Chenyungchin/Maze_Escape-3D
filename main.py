import sys, time
import random
import pygame
from pygame.locals import Color, QUIT, MOUSEBUTTONDOWN, USEREVENT, USEREVENT
from maze_2D import build_grid, generate_maze

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
screen.fill(white)
pygame.display.set_caption("Maze Escape-3D")
clock = pygame.time.Clock()





mapsize = "12x9"

if mapsize == "12x9":
    w = 720 // 12
    width = 12
    height = 9
elif mapsize == "16x12":
    w = 720 // 16
    width = 16
    height = 12
elif mapsize == "20x15":
    w = 720 // 20
    width = 20
    height = 15

test = False
if test:
    w = 720 // 4
    width = 4
    height = 3

build_grid(width, height, w)
algorithm = "dfs_backtrack"
# algorithm = "randomized_kruskal"
# algorithm = "randomized_prims"
maze_matrix = generate_maze(algorithm, width, height, w)

for i in range(2*height-1):
    maze_matrix[i].insert(0, 1)
    maze_matrix[i].append(1)
maze_matrix.insert(0, [1]*(2*width+1))
maze_matrix.append([1]*(2*width+1))
#define starting point
maze_matrix[1][0] = 0


print(maze_matrix)



run = True
while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        # check for closing the window
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

