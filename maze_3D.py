import pygame as pg
from pygame.locals import *
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *
from objloader import *

cubeVertices = [[1,1,1],[1,1,-1],[1,-1,-1],[1,-1,1],[-1,1,1],[-1,-1,-1],[-1,-1,1],[-1,1,-1]]
cubeEdges = ((0,1),(0,3),(0,4),(1,2),(1,7),(2,5),(2,3),(3,6),(4,6),(4,7),(5,6),(5,7))
cubeQuads = ((0,3,6,4),(2,5,6,3),(1,2,5,7),(1,0,4,7),(7,4,6,5),(2,3,0,1))

def wireCube(map):
    glBegin(GL_LINES)
    glColor3f(1.0, 1.0, 1.0)
    for i in range(len(map)):
        for k in range(len(map[0])):
            for vertice in cubeVertices:
                vertice[0]-=i*2
                vertice[2]-=k*2
            if map[i][k] == 1:
                for cubeEdge in cubeEdges:
                    for cubeVertex in cubeEdge:
                        glVertex3fv(cubeVertices[cubeVertex])
            for vertice in cubeVertices:
                vertice[0]+=i*2
                vertice[2]+=k*2
    glEnd()

def solidCube(map):
    glBegin(GL_QUADS)
    for i in range(len(map)):
        for k in range(len(map[0])):
            for vertice in cubeVertices:
                vertice[0]-=i*2
                vertice[2]-=k*2
            if map[i][k] == 1:
                for cubeQuad in cubeQuads:
                    for cubeVertex in cubeQuad:
                        glVertex3fv(cubeVertices[cubeVertex])
            for vertice in cubeVertices:
                vertice[0]+=i*2
                vertice[2]+=k*2
    glEnd()

def draw_ball(x, y, z, r):
    glPushMatrix()

    glTranslate(x, y, z)

    q = gluNewQuadric()
    gluSphere(q, r, 20, 20)
    gluDeleteQuadric(q)

    glPopMatrix()

def collision_detect(map, x, z):
    bias = 0.0
    print(x, z, round((x+bias)/2), round((z+bias)/2))
    if round((x+bias)/2) >= 0 and round((z+bias)/2) >= 0:
        if map[round((x+bias)/2)][round((z+bias)/2)] == 1:
            return True
    

def main(map, display):
    pg.init()
    # display = (1680, 1050)
    pg.display.set_mode(display, DOUBLEBUF|OPENGL)

    glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 200, 100, 0.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)           # most obj files expect to be smooth-shaded
    # LOAD OBJECT AFTER PYGAME INIT
    obj = OBJ("Ghost.obj", swapyz=True)
    obj.generate(scale_rate = 0.1, rx=-90, rz=0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_MODELVIEW)

    x = 0.0
    z = -5.0
    glTranslatef(x, 0.0, z)
    vz = 0
    vx = 0
    bx = -3
    bz = -5
    print("in loop")
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    vz+=0.1
                elif event.key == pg.K_DOWN:
                    vz-=0.1
                elif event.key == pg.K_RIGHT:
                    vx -= 0.1
                elif event.key == pg.K_LEFT:
                    vx += 0.1
                elif event.key == pg.K_SPACE:
                    glTranslatef(-x, 0.0, -z)
                    x = 0.0
                    z = 0.0
            if event.type == pg.KEYUP:
                if event.key == pg.K_UP:
                    vz-=0.1
                elif event.key == pg.K_DOWN:
                    vz+=0.1
                elif event.key == pg.K_RIGHT:
                    vx += 0.1
                elif event.key == pg.K_LEFT:
                    vx -= 0.1
        x += vx
        z += vz
        bx -= vx
        bz -= vz
        if vx != 0 or vz != 0:
            if collision_detect(map, x, z):
                x -= vx
                z -= vz
            else:
                glTranslatef(vx, 0.0, vz)
            if collision_detect(map, -bx, -bz):
                print("collide")
                bx += vx
                bz += vz
            
        # glRotatef(1, 1, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        solidCube(map)
        # obj.generate(scale_rate = 0.1, rx=-90, rz=0)
        # obj.render()
        draw_ball(x=bx, y=-0.7, z=bz, r=0.3)
        # wireCube(map)
        pg.display.flip()
        # pg.time.wait(10)