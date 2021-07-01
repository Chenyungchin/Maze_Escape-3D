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
    if (x-bx)**2 + (z-bz)**2 < 0.5:
        return True
    else:
        return False

def calculate_pos(x, z):
    # print("("+str(round(x/2))+","+str(round(z/2))+")")
    return((round(x/2), round(z/2)))

def handel_key(event, vx, vz, step, theta, dtheta, theta_step):
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
        # elif event.key == pg.K_SPACE:
        #     glTranslatef(-x, 0.0, -z)
        #     x = 0.0
        #     z = 0.0
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
    
    return vx, vz, step, theta, dtheta, theta_step

def enemy_moving(path, x, z):
    z_next, x_next = path[0]
    z_next*=2
    x_next*=2
    print(path, x, z)
    vbx = 0
    vbz = 0
    if x_next - x <= -0.019:
        vbx = -0.05
    elif x_next - x >= 0.019:
        vbx = 0.05
    if z_next - z <= -0.019:
        vbz = -0.05
    elif z_next - z >= 0.019:
        vbz = 0.05
    return vbx, vbz
    

def main(map, display):
    pg.init()
    # display = (1680, 1050)
    pg.display.set_mode(display, DOUBLEBUF|OPENGL)
    Maze = maze(map=map)
    init(display)
    # LOAD OBJECT AFTER PYGAME INIT
    obj = OBJ("obj/ghost.obj", swapyz=True)
    obj.generate(scale_rate = 1, rx=-90, rz=0)
    # glMatrixMode(GL_PROJECTION)
    # glLoadIdentity()

    # gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    # glEnable(GL_DEPTH_TEST)
    # glMatrixMode(GL_MODELVIEW)
    x = 2
    z = 0
    vz = 0
    vx = 0
    bx = 4
    bz = 6
    vbx = 0
    vbz = 0
    theta = 0
    dtheta = 0
    theta_step = 5
    step = 0.5
    path = shortest_path_bfs(
        maze_matrix=Maze.map, 
        start=calculate_pos(bz, bx),
        end=calculate_pos(z, x),
        maze_width=len(Maze.map[0]),
        maze_height=len(Maze.map)
    )
    glTranslatef(x, 0.0, z)
    # texture = Texture()
    # wall_texture = texture.loadImage("tex/wall2.bmp")
    # pacman = texture.loadImage("tex/pacman.bmp")
    while True:
        if game_over(x, z, bx, bz):
            print("game over idiot")
            return True
        for event in pg.event.get():
            vx, vz, step, theta, dtheta, theta_step = handel_key(
                event, vx, vz, step, theta, dtheta, theta_step)
                        
        x += vx
        z += vz
        # bx += vx
        # bz += vz
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
            if Maze.collision_detect(x, z):
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
            if Maze.collision_detect(bx, bz):
                # print("collide")
                bx -= vx
                bz -= vz
         
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
        print(bx, bz, vbx, vbz)

        if dtheta != 0:
            glTranslatef(-x, 0.0, -z)
            glRotatef(dtheta, 0, 1, 0)
            glTranslatef(x, 0.0, z)
            # print(theta)
        # calculate_pos(-bx, -bz)
        # print(theta, vx, vz)
        # glRotatef(1, 1, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        obj.generate(scale_rate = 0.1, rx=-90, rz=0, mx=bx, mz=bz)
        # glColor3f(0.0, 0.9, 0.0)
        obj.render()
        # draw_ball(x=bx, y=-0.7, z=bz, r=0.3)
        Maze.solidCube()
        # print(shortest_path_bfs(
        #     maze_matrix=Maze.map, 
        #     start=calculate_pos(x, z),
        #     end=calculate_pos(bx, bz),
        #     maze_width=len(Maze.map[0]),
        #     maze_height=len(Maze.map)
        # ))
        # wireCube(map)
        pg.display.flip()
        # pg.time.wait(10)