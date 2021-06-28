import sys, time
import random
import pygame
from pygame.locals import Color, QUIT, MOUSEBUTTONDOWN, USEREVENT, USEREVENT
from disjoint_set import initialize, merge, find

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
yellow = (255,255,0)

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# x = 40
# y = 30
grid = []

# build the grid
def build_grid(width, height, w):
    x = 40
    y = 30
    for i in range(height):
        for j in range(width):
            pygame.draw.line(screen, black, (x, y), (x + w, y))
            pygame.draw.line(screen, black, (x + w, y), (x + w, y + w))
            pygame.draw.line(screen, black, (x + w, y + w), (x, y + w))
            pygame.draw.line(screen, black, (x, y + w), (x, y))
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

def go_right(x, y, w):
    pygame.draw.rect(screen, blue_violet,(x+1, y+1, 2*w-1, w-1))
    pygame.display.update()

def go_left(x, y, w):
    pygame.draw.rect(screen, blue_violet,(x-w+1, y+1, 2*w-1, w-1))
    pygame.display.update()

def go_up(x, y, w):
    pygame.draw.rect(screen, blue_violet,(x+1, y-w+1, w-1, 2*w-1))
    pygame.display.update()

def go_down(x, y, w):
    pygame.draw.rect(screen, blue_violet,(x+1, y+1, w-1, 2*w-1))
    pygame.display.update()

def highlight_coloring(x, y, w):
    pygame.draw.rect(screen, yellow,(x+1, y+1, w-1, w-1))
    pygame.display.update()

def cell_recoloring(x, y, w):
    pygame.draw.rect(screen, blue_violet,(x+1, y+1, w-1, w-1))
    pygame.display.update()

def generate_maze(algorithm, width, height, w):
    maze_matrix = [[(i+j)%2 for j in range(2*width-1)] for i in range(2*height-1)]
    if algorithm == "dfs_backtrack":
        return dfs_backtrack(w, maze_matrix)
    if algorithm == "randomized_kruskal":
        return randomized_kruskal(width, height, w, maze_matrix)
    if algorithm == "randomized_prims":
        return randomized_prims(width, height, w, maze_matrix)

def dfs_backtrack(w, maze_matrix):
    x = 40
    y = 30
    cell_stack = [(x, y)]
    visited = [(x, y)]
    while len(cell_stack) > 0:
        time.sleep(0.1)
        cell_recoloring(x, y, w)
        directions = []
        if (x+w, y) in grid and (x+w, y) not in visited:
            directions.append("right")
        if (x-w, y) in grid and (x-w, y) not in visited:
            directions.append("left")
        if (x, y+w) in grid and (x, y+w) not in visited:
            directions.append("down")
        if (x, y-w) in grid and (x, y-w) not in visited:
            directions.append("up")

        if directions:
            direction = random.choice(directions)

            if direction == "right":
                go_right(x, y, w)
                col = (x-40)//w
                row = (y-30)//w
                maze_matrix[2*row][2*col+1] = 0
                x += w
            elif direction == "left":
                go_left(x, y, w)
                col = (x-w-40)//w
                row = (y-30)//w
                maze_matrix[2*row][2*col+1] = 0
                x -= w
            elif direction == "down":
                go_down(x, y, w)
                col = (x-40)//w
                row = (y-30)//w
                maze_matrix[2*row+1][2*col] = 0
                y += w
            else:
                go_up(x, y, w)
                col = (x-40)//w
                row = (y-w-30)//w
                maze_matrix[2*row+1][2*col] = 0
                y -= w

            visited.append((x, y))
            cell_stack.append((x, y))
        else:
            (x, y) = cell_stack.pop()
            highlight_coloring(x, y, w)
    cell_recoloring(x, y, w)
    return maze_matrix


def randomized_kruskal(width, height, w, maze_matrix):
    x = 40
    y = 30
    leader, rank, edges = initialize(width, height)
    n = width*height
    for i in range(n-1):
        time.sleep(0.2)
        while True:
            rand_edge = random.choice(edges)
            edges.remove(rand_edge)
            cell1, cell2 = rand_edge
            if merge(cell1, cell2, leader, rank):
                row = cell1//width
                col = cell1%width
                x = 40 + col*w
                y = 30 + row*w
                if cell2-cell1 == 1:
                    go_right(x, y, w)
                    maze_matrix[2*row][2*col+1] = 0
                else:
                    go_down(x, y, w)
                    maze_matrix[2*row+1][2*col] = 0
                break
    return maze_matrix

def randomized_prims(width, height, w, maze_matrix):
    x = 40
    y = 30
    movement_list = [(x, y, "right"), (x, y, "down")]
    visited = [(x, y)]
    while len(movement_list) > 0:
        movement = random.choice(movement_list)
        x, y, direction = movement
        movement_list.remove(movement)
        if (x, y) in grid and (x, y) not in visited:
            highlight_coloring(x, y, w)
            time.sleep(0.1)
            visited.append((x, y))
            if direction == "right":
                go_right(x-w, y, w)
                col = (x-w-40)//w
                row = (y-30)//w
                maze_matrix[2*row][2*col+1] = 0
            elif direction == "left":
                go_left(x+w, y, w)
                col = (x-40)//w
                row = (y-30)//w
                maze_matrix[2*row][2*col+1] = 0
            elif direction == "down":
                go_down(x, y-w, w)
                col = (x-40)//w
                row = (y-w-30)//w
                maze_matrix[2*row+1][2*col] = 0
            else:#up
                col = (x-40)//w
                row = (y-30)//w
                maze_matrix[2*row+1][2*col] = 0
                go_up(x, y+w, w)

        if (x+w, y) in grid and (x+w, y) not in visited:
            movement_list.append((x+w, y, "right"))
        if (x-w, y) in grid and (x-w, y) not in visited:
            movement_list.append((x-w, y, "left"))
        if (x, y+w) in grid and (x, y+w) not in visited:
            movement_list.append((x, y+w, "down"))
        if (x, y-w) in grid and (x, y-w) not in visited:
            movement_list.append((x, y-w, "up"))

    return maze_matrix
        




