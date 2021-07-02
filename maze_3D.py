import pygame as pg
from pygame.locals import *
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *
from objloader import *
from src.texture import Texture
import math
from src.map import maze
from maze_2D import shortest_path_bfs

def init(display):
    glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 200, 100, 0.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)           # most obj files expect to be smooth-shaded
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_MODELVIEW)

def draw_ball(x, y, z, r, texture_id=None):
    glPushMatrix()
    glTranslate(x, y, z)
    # glBindTexture(GL_TEXTURE_2D, texture_id)
    q = gluNewQuadric()
    # gluQuadricTexture(q, GL_TRUE)
    gluSphere(q, r, 20, 20)
    gluDeleteQuadric(q)
    glPopMatrix()

def game_over(x, z, bx, bz):
    # print("pos", (x, z), (bx, bz))
    if (x-bx)**2 + (z-bz)**2 < 0.8:
        return True
    else:
        return False

def win(x, z, tx, tz):
    if (x-tx)**2 + (z-tz)**2 <= 1:
        return True
    else:
        return False

def calculate_pos(x, z):
    # print("("+str(round(x/2))+","+str(round(z/2))+")")
    return (round(x/2), round(z/2))

def handel_key(event, vx, vy, vz, y, step, theta, dtheta, theta_step):
    if event.type == pg.QUIT:
        pg.quit()
        quit()
    if event.type == pg.KEYDOWN:
        if event.key == pg.K_UP:
            vz+=step*math.cos(math.pi/180*theta)
            vx-=step*math.sin(math.pi/180*theta)
        elif event.key == pg.K_DOWN:
            vz-=step*math.cos(math.pi/180*theta)
            vx+=step*math.sin(math.pi/180*theta)
        elif event.key == pg.K_RIGHT:
            # vx -= step
            dtheta += theta_step
        elif event.key == pg.K_LEFT:
            # vx += step
            dtheta -= theta_step
        elif event.key == pg.K_SPACE:
            if y==0:
                print("jump")
                vy = 0.6
    if event.type == pg.KEYUP:
        if event.key == pg.K_UP:
            vz-=step*math.cos(math.pi/180*theta)
            vx+=step*math.sin(math.pi/180*theta)
        elif event.key == pg.K_DOWN:
            vz+=step*math.cos(math.pi/180*theta)
            vx-=step*math.sin(math.pi/180*theta)
        elif event.key == pg.K_RIGHT:
            # vx += step
            dtheta -= theta_step
        elif event.key == pg.K_LEFT:
            # vx -= step
            dtheta += theta_step
    
    return vx, vy, vz, step, theta, dtheta, theta_step

def enemy_moving(path, x, z):
    z_next, x_next = path[0]
    z_next*=2
    x_next*=2
    v = 0.1
    print(path, x, z)
    vbx = 0
    vbz = 0
    if x_next - x <= -0.019:
        vbx = -v
    elif x_next - x >= 0.019:
        vbx = v
    if z_next - z <= -0.019:
        vbz = -v
    elif z_next - z >= 0.019:
        vbz = v
    return vbx, vbz

def go_to_next_pipe(x, y, z, Maze):
    x_next, z_next = Maze.get_next_pipe(x, z)
    # glPushMatrix()
    # glTranslatef(x, 0.5, z)
    # for i in range(2):
    #     pg.time.wait(300)
    #     glTranslatef(0, -0.5, 0)
    #     glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    # glPopMatrix()
    # glPushMatrix()
    glTranslatef(x_next-x, 1-y, z_next-z)
    # pg.time.wait(300)
    # glTranslatef(x_next, -0.5, z_next)
    # for i in range(2):
    #     pg.time.wait(300)
    #     glTranslatef(0, 0.5, 0)
    #     glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    # glPopMatrix()
    
    return x_next, 1, z_next


def main(map, display):
    # pg.init()
#     # display = (1680, 1050)
    pg.display.set_mode(display, DOUBLEBUF|OPENGL)
    texture = Texture()
    wall_texture = texture.loadImage("tex/wall.jpeg")
    ceil_texture = texture.loadImage("tex/top.png")
    floor_texture = texture.loadImage("tex/floor_01.png")
    Maze = maze(map=map, cube=wall_texture, floor=floor_texture, ceil=ceil_texture)
    init(display)
    # LOAD OBJECT AFTER PYGAME INIT
    obj = OBJ("obj/ghost.obj", swapyz=True)
    obj.generate(scale_rate = 5, rx=-90, rz=0)
    # trophy = OBJ("obj/trophy.obj", swapyz=True)
    # trophy.generate(scale_rate = 0.1, rx=-90, rz=90, mx=len(map)*2-2, mz=len(map[0])*2-4)
    pipe_pos = Maze.get_pipe()
    pipe1 = OBJ("obj/MarioPipe.obj", swapyz=True)
    pipe1.generate(scale_rate=0.01, rx=-90, mx=pipe_pos[0][0], mz=pipe_pos[0][1], my=1)
    pipe2 = OBJ("obj/MarioPipe.obj", swapyz=True)
    pipe2.generate(scale_rate=0.01, rx=-90, mx=pipe_pos[1][0], mz=pipe_pos[1][1], my=1)

    x = 2
    y = 0
    z = 0
    vz = 0
    vy = 0
    vx = 0
    g = 0.05
    bx = 10
    bz = 10
    vbx = 0
    vbz = 0
    theta = 0
    dtheta = 0
    theta_step = 10
    step = 0.5
    passed = False
    player_path = [(z//2, x//2)]
    path = shortest_path_bfs(
        maze_matrix=Maze.map, 
        start=calculate_pos(bz, bx),
        end=calculate_pos(z, x),
        maze_width=len(Maze.map[0]),
        maze_height=len(Maze.map)
    )
    glTranslatef(x, 0.0, z)
    
    # pacman = texture.loadImage("tex/pacman.bmp")
    while True:
        if game_over(x, z, bx, bz):
            return False, player_path
        if win(x, z, len(map)*2-2, len(map[0])*2-4):
            return True, player_path
        for event in pg.event.get():
            vx, vy, vz, step, theta, dtheta, theta_step = handel_key(
                event, vx, vy, vz, y, step, theta, dtheta, theta_step)
                        
        x += vx
        z += vz
        theta += dtheta
        if dtheta != 0:
            if vx != 0:
                vx /= math.sin(math.pi/180*(theta-dtheta))
                vx *= math.sin(math.pi/180*theta)
            elif vz != 0:
                vx -= step*math.sin(math.pi/180*theta)
            if vz != 0:
                vz /= math.cos(math.pi/180*(theta-dtheta))
                vz *= math.cos(math.pi/180*theta)
            elif vx != 0:
                vz += step*math.cos(math.pi/180*theta)
        if vx != 0 or vz != 0:
            if Maze.on_pipe(x, z, y):
                if not passed:
                    x, y, z = go_to_next_pipe(x, y, z, Maze)
                    vy = 0
                    passed = True
            else:
                passed = False
            if Maze.collision_detect(x, y, z):
                # print("True")
                x -= vx
                z -= vz
            else:
                # print(theta, vx, vz)
                glTranslatef(vx, 0.0, vz)
                path = shortest_path_bfs(
                    maze_matrix=Maze.map, 
                    start=calculate_pos(bz, bx),
                    end=calculate_pos(z, x),
                    maze_width=len(Maze.map[0]),
                    maze_height=len(Maze.map)
                )
                path.pop(0)
         
        if path != []:
            if path[0] == (bz/2, bx/2):
                path.pop(0)
            if path != []:
                vbx, vbz = enemy_moving(path, bx, bz)
        else:
            vbx = 0
            vbz = 0
        bx += vbx
        bz += vbz
        bx = round(bx, 2)
        bz = round(bz, 2)
        # print(y, vy)

        if dtheta != 0:
            glTranslatef(-x, 0.0, -z)
            glRotatef(dtheta, 0, 1, 0)
            glTranslatef(x, 0.0, z)
            # print(theta)
        # calculate_pos(-bx, -bz)
        # print(theta, vx, vz)
        if not Maze.on_pipe(x, z, y):
            if y > 0:
                vy -= g
                # print("vy:", vy)
                if y+vy > 0:
                    glTranslatef(0, -vy, 0)
                else:
                    glTranslatef(0, y, 0)
                y = max(y+vy, 0)
            if y == 0:
                vy = max(vy, 0)
                glTranslatef(0, -vy, 0)
                y += vy

        if calculate_pos(z, x) != player_path[-1]:
            player_path.append(calculate_pos(z, x))
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        obj.generate(scale_rate = 0.1, rx=-90, rz=0, mx=bx, mz=bz)
        obj.render()
        # trophy.render()
        pipe1.render()
        pipe2.render()
        Maze.solidCube(calculate_pos(x, z))
        Maze.draw_plane(50)
        Maze.draw_ceil()
        pg.display.flip()
