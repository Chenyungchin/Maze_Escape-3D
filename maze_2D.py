import sys, time
import random
import pygame
from pygame.locals import Color, QUIT, MOUSEBUTTONDOWN, USEREVENT, USEREVENT
from disjoint_set import initialize, merge, find
import queue

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

bias_x = 24
bias_y = 18
grid = []

# build the grid
def build_grid(width, height, w):
    x = bias_x
    y = bias_y
    for i in range(height):
        for j in range(width):
            pygame.draw.line(screen, black, (x, y), (x + w, y))
            pygame.draw.line(screen, black, (x + w, y), (x + w, y + w))
            pygame.draw.line(screen, black, (x + w, y + w), (x, y + w))
            pygame.draw.line(screen, black, (x, y + w), (x, y))
            grid.append((x,y))
            x = x + w
        x = bias_x
        y += w
    
    # pygame.display.update()

def remove_horizontal(x, y, w):
    pygame.draw.line(screen, blue_violet, (x, y), (x + w, y))
    # pygame.display.update()

def remove_vertical(x, y, w):
    pygame.draw.line(screen, blue_violet, (x, y), (x, y + w))
    # pygame.display.update()

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
    maze_matrix = [[1 for j in range(2*width-1)] for i in range(2*height-1)]
    for j in range(2*height-1):
        for i in range(2*width-1):
            if i%2 == 0 and j%2 == 0:
                maze_matrix[j][i] = 0
    if algorithm == "dfs_backtrack":
        return dfs_backtrack(w, maze_matrix)
    if algorithm == "randomized_kruskal":
        return randomized_kruskal(width, height, w, maze_matrix)
    if algorithm == "randomized_prims":
        return randomized_prims(width, height, w, maze_matrix)

def maze_drawing2D(draw_step, algorithm, locations, maze_width, maze_height):
    while len(draw_step) > 0:
        if algorithm == "dfs_backtrack":
            delay = 0.05
        else:
            delay = 0.1
        test = False
        if test:
            delay = 0.0001
        time.sleep(delay)
        x, y, w, direction = draw_step.pop(0)
        if direction == "highlight":
            highlight_coloring(x, y, w)
        elif direction == "right":
            go_right(x, y, w)
        elif direction == "left":
            go_left(x, y, w)
        elif direction == "down":
            go_down(x, y, w)
        elif direction == "up":
            go_up(x, y, w)
        elif direction == "recolor":
            cell_recoloring(x, y, w)

    bias_x = 24
    bias_y = 18
    delay = 0.5
    if test:
        delay = 0.001
    icons = ["./resources/start.png", "./resources/ghost.png", "./resources/pipe.png", "./resources/pipe.png", "./resources/trophy.png"]
    locations_all = [(1, 1), locations[0], locations[1], locations[2], (maze_width-2, maze_height-2)]
    for index, url in enumerate(icons):
        icon = pygame.image.load(url).convert_alpha()
        icon = pygame.transform.scale(icon, (w, w))
        col, row = locations_all[index]
        x, y = bias_x+((col-1)//2)*w, bias_y+((row-1)//2)*w
        screen.blit(icon, (x, y))
        pygame.display.update()
        time.sleep(delay)
    

 

        

def dfs_backtrack(w, maze_matrix):
    x = bias_x
    y = bias_y
    cell_stack = [(x, y)]
    visited = [(x, y)]
    draw_step = []
    while len(cell_stack) > 0:
        # time.sleep(0.1)
        # cell_recoloring(x, y, w)
        draw_step.append((x, y, w, "recolor"))
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
                # go_right(x, y, w)
                draw_step.append((x, y, w, "right"))
                col = (x-bias_x)//w
                row = (y-bias_y)//w
                maze_matrix[2*row][2*col+1] = 0
                x += w
            elif direction == "left":
                # go_left(x, y, w)
                draw_step.append((x, y, w, "left"))
                col = (x-w-bias_x)//w
                row = (y-bias_y)//w
                maze_matrix[2*row][2*col+1] = 0
                x -= w
            elif direction == "down":
                # go_down(x, y, w)
                draw_step.append((x, y, w, "down"))
                col = (x-bias_x)//w
                row = (y-bias_y)//w
                maze_matrix[2*row+1][2*col] = 0
                y += w
            else:
                # go_up(x, y, w)
                draw_step.append((x, y, w, "up"))
                col = (x-bias_x)//w
                row = (y-w-bias_y)//w
                maze_matrix[2*row+1][2*col] = 0
                y -= w

            visited.append((x, y))
            cell_stack.append((x, y))
        else:
            (x, y) = cell_stack.pop()
            # highlight_coloring(x, y, w)
            draw_step.append((x, y, w, "highlight"))
    # cell_recoloring(x, y, w)
    draw_step.append((x, y, w, "recolor"))
    return maze_matrix, draw_step


def randomized_kruskal(width, height, w, maze_matrix):
    x = bias_x
    y = bias_y
    leader, rank, edges = initialize(width, height)
    draw_step = []
    n = width*height
    for i in range(n-1):
        #time.sleep(0.2)
        while True:
            rand_edge = random.choice(edges)
            edges.remove(rand_edge)
            cell1, cell2 = rand_edge
            if merge(cell1, cell2, leader, rank):
                row = cell1//width
                col = cell1%width
                x = bias_x + col*w
                y = bias_y + row*w
                if cell2-cell1 == 1:
                    draw_step.append((x, y, w, "right"))
                    maze_matrix[2*row][2*col+1] = 0
                else:
                    draw_step.append((x, y, w, "down"))
                    maze_matrix[2*row+1][2*col] = 0
                break
    return maze_matrix, draw_step
        

def randomized_prims(width, height, w, maze_matrix):
    x = bias_x
    y = bias_y
    movement_list = [(x, y, "right"), (x, y, "down")]
    visited = [(x, y)]
    draw_step = []
    while len(movement_list) > 0:
        movement = random.choice(movement_list)
        x, y, direction = movement
        movement_list.remove(movement)
        if (x, y) in grid and (x, y) not in visited:
            # highlight_coloring(x, y, w)
            draw_step.append((x, y, w, "highlight"))
            # time.sleep(0.1)
            visited.append((x, y))
            if direction == "right":
                # go_right(x-w, y, w)
                draw_step.append((x-w, y, w, "right"))
                col = (x-w-bias_x)//w
                row = (y-bias_y)//w
                maze_matrix[2*row][2*col+1] = 0
            elif direction == "left":
                # go_left(x+w, y, w)
                draw_step.append((x+w, y, w, "left"))
                col = (x-bias_x)//w
                row = (y-bias_y)//w
                maze_matrix[2*row][2*col+1] = 0
            elif direction == "down":
                # go_down(x, y-w, w)
                draw_step.append((x, y-w, w, "down"))
                col = (x-bias_x)//w
                row = (y-w-bias_y)//w
                maze_matrix[2*row+1][2*col] = 0
            else:#up
                draw_step.append((x, y+w, w, "up"))
                col = (x-bias_x)//w
                row = (y-bias_y)//w
                maze_matrix[2*row+1][2*col] = 0
                # go_up(x, y+w, w)

        if (x+w, y) in grid and (x+w, y) not in visited:
            movement_list.append((x+w, y, "right"))
        if (x-w, y) in grid and (x-w, y) not in visited:
            movement_list.append((x-w, y, "left"))
        if (x, y+w) in grid and (x, y+w) not in visited:
            movement_list.append((x, y+w, "down"))
        if (x, y-w) in grid and (x, y-w) not in visited:
            movement_list.append((x, y-w, "up"))

    return maze_matrix, draw_step
        
def shortest_path_bfs(maze_matrix, start, end, maze_width, maze_height):
    Q = queue.Queue()
    Q.put(start)
    # print(Q.qsize())
    visit = [start]
    ancestor = [[0 for j in range(maze_width)] for i in range(maze_height)]
    while end not in visit:
        x, y = Q.get()
        # print(x, y, Q.qsize())
        if x+1 <= maze_width-1 and maze_matrix[y][x+1] == 0 and (x+1, y) not in visit:
            Q.put((x+1, y))
            visit.append((x+1, y))
            ancestor[y][x+1] = (x, y)
        if x-1 >= 0 and maze_matrix[y][x-1] == 0 and (x-1, y) not in visit:
            Q.put((x-1, y))
            visit.append((x-1, y))
            ancestor[y][x-1] = (x, y)
        if y+1 <= maze_height-1 and maze_matrix[y+1][x] == 0 and (x, y+1) not in visit:
            Q.put((x, y+1))
            visit.append((x, y+1))
            ancestor[y+1][x] = (x, y)
        if y-1 >= 0 and maze_matrix[y-1][x] == 0 and (x, y-1) not in visit:
            Q.put((x, y-1))
            visit.append((x, y-1))
            ancestor[y-1][x] = (x, y)
    
    path = [end]
    location = end
    while start != end:
        location = ancestor[location[1]][location[0]]
        path.insert(0, location)
        if location == start:
            break
    return path


def define_locations(maze_matrix, maze_width, maze_height):
    sx, sy = (0, 1)
    ex, ey = (maze_width-2, maze_height-1)
    while True:
        ghostx = random.randint(1, maze_width-2)
        ghosty = random.randint(1, maze_height-2)
        if abs(ghostx-ex) + abs(ghosty-ey) <= (maze_width+maze_height)/4 and maze_matrix[ghosty][ghostx] == 0:
            break
    while True:
        pipex1 = random.randint(1, maze_width-2)
        pipey1 = random.randint(1, maze_height-2)
        if abs(pipex1-sx) + abs(pipey1-sy) >= (maze_width+maze_height)/5 and abs(pipex1-ex) + abs(pipey1-ey) >= (maze_width+maze_height)/5 and maze_matrix[pipey1][pipex1] == 0:
            break
    while True:
        pipex2 = random.randint(1, maze_width-2)
        pipey2 = random.randint(1, maze_height-2)
        if abs(pipex2-sx) + abs(pipey2-sy) >= (maze_width+maze_height)/5 and abs(pipex2-ex) + abs(pipey2-ey) >= (maze_width+maze_height)/5 and abs(pipex1-pipex2) + abs(pipey1-pipey2) >= (maze_width+maze_height)/3 and maze_matrix[pipey2][pipex2] == 0:
            break

    return (ghostx, ghosty), (pipex1, pipey1), (pipex2, pipey2)

def auxiliary_map(player, ghost, pipe1, pipe2, maze_width, maze_height):
    # start, end, player, ghost, pipe1, pipe2
    map_width = 160
    map_height = 120
    bias_x = 1024-map_width
    bias_y = 0
    wx = round(map_width/maze_width)
    wy = round(map_height/maze_height)
    
    pygame.draw.rect(screen, blue_violet,(bias_x, 0, map_width, map_height))
    positions = [(0, 1), (maze_width-2, maze_height-1), player, ghost, pipe1, pipe2]
    icons = ["./resources/start.png", "./resources/trophy.png", "./resources/player.png", "./resources/ghost.png", "./resources/pipe.png", "./resources/pipe.png"]
    
    for index, url in enumerate(icons):
        icon = pygame.image.load(url).convert_alpha()
        icon = pygame.transform.scale(icon, (3*wx, 3*wy))
        col, row = positions[index]
        x, y = bias_x+col*wx, bias_y+row*wy
        screen.blit(icon, (x, y-wy))




if __name__ == "__main__":

    width = 12
    height = 9
    w = 720 // width

    
    maze = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
  [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1], 
  [1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1], 
  [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1], 
  [1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1], 
  [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1], 
  [1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1], 
  [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1], 
  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1], 
  [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1], 
  [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1], 
  [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1], 
  [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1], 
  [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1], 
  [1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1], 
  [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1], 
  [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1], 
  [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1], 
  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1]] 

    

    dao = define_locations(maze, 25, 19)

    print(dao)
    


# (1, 9) (2, 11) 25 19
