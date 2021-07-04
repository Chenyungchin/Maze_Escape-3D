import pygame as pg
from pygame.locals import *
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *
from objloader import *
import math
import numpy as np
from PIL import Image

cubeVertices = [[1,1,1],[1,1,-1],[1,-1,-1],[1,-1,1],[-1,1,1],[-1,-1,-1],[-1,-1,1],[-1,1,-1]]
cubeTextures = [[0, 0], [0, 1], [1, 1], [1, 0]]
cubeEdges = ((0,1),(0,3),(0,4),(1,2),(1,7),(2,5),(2,3),(3,6),(4,6),(4,7),(5,6),(5,7))
cubeQuads = ((0,3,6,4),(2,5,6,3),(1,2,5,7),(1,0,4,7),(7,4,6,5),(2,3,0,1))

class maze:
    def __init__(self, map, location, cube = None, floor = None, ceil = None, pipe=None, ghost=None, trophy=None, player=None, start=None):
        # map = np.array(map).T
        # map = list(map)
        # for i in range(len(map)):
        #     map[i] = list(map[i])
        self.map = map
        self.cube = cube
        self.floor = floor
        self.ceil = ceil
        self.pipe_texture = pipe
        self.ghost = ghost
        self.trophy = trophy
        self.player = player
        self.start = start
        self.add_pipe(location[1:])
        print(self.map)
        self.pipe = []
        for i in range(len(map)):
            for k in range(len(map[0])):
                if map[i][k] == 2:
                    self.pipe.append((i*2, k*2))

    def draw_plane(self, texture_tile=1):
        glPushMatrix()
        glScalef(len(self.map)*4, 1.0, len(self.map[0])*4)
        if self.floor is not None:
            glEnable(GL_TEXTURE_2D)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
            # Repeat the texture.
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);

            glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

            glBindTexture(GL_TEXTURE_2D, self.floor)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0,-1.0);
        glTexCoord2f(texture_tile, 0.0); glVertex3f(-1.0, -1.0,-1.0);
        glTexCoord2f(texture_tile, texture_tile); glVertex3f(-1.0, -1.0, 1.0);
        glTexCoord2f(0.0, texture_tile); glVertex3f( 1.0, -1.0, 1.0);
        glEnd()
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()
    
    def draw_ceil(self, texture_tile=1):
        glPushMatrix()
        # glScalef(len(self.map)*4, 1.0, len(self.map[0])*4)
        if self.ceil is not None:
            glEnable(GL_TEXTURE_2D)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
            # Repeat the texture.
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);

            glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

            glBindTexture(GL_TEXTURE_2D, self.ceil)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0); glVertex3f( -len(self.map)*4, 4.0,len(self.map));
        glTexCoord2f(texture_tile, 0.0); glVertex3f(len(self.map), 4.0,len(self.map));
        glTexCoord2f(texture_tile, texture_tile); glVertex3f(len(self.map), 4.0, -len(self.map)*4);
        glTexCoord2f(0.0, texture_tile); glVertex3f( -len(self.map)*4, 4.0, -len(self.map)*4);
        glEnd()
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()

    def draw_pic(self, texture, x, y, size=20):
        if self.ceil is not None:
            glEnable(GL_TEXTURE_2D)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
            # Repeat the texture.
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);

            glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

            glBindTexture(GL_TEXTURE_2D, texture)
        glBegin(GL_QUADS)
        # glColor3f(1.0, 1.0, 1.0)
        glTexCoord2f(0.0, 0.0); glVertex3f(x+size/2, y-size/2, 0)
        glTexCoord2f(1.0, 0.0); glVertex3f(x+size/2, y+size/2, 0)
        glTexCoord2f(1.0, 1.0); glVertex3f(x-size/2, y+size/2, 0)
        glTexCoord2f(0.0, 1.0); glVertex3f(x-size/2, y-size/2, 0)
        glEnd()
        glDisable(GL_TEXTURE_2D)

    def draw_square(self, pipe1_pos, pipe2_pos, ghost_pos, trophy_pos, player_pos):
        # glDisable(GL_TEXTURE_2D)
        mapH = 150
        mapW = 200
        bias_w = 1024-mapW
        bias_h = 576-mapH
        glBegin(GL_QUADS)
        glColor3f(2.0, 2.0, 2.0)
        glVertex3f(mapW+bias_w, bias_h-12, 0)
        glVertex3f(mapW+bias_w, mapH+bias_h, 0)
        glVertex3f(bias_w-20, mapH+bias_h, 0)
        glVertex3f(bias_w-20, bias_h-12, 0)
        glEnd()

        # positions = [(0, 1), trophy_pos, player_pos, ghost_pos, pipe1_pos, pipe2_pos]
        positions = [(1, 0), pipe1_pos, pipe2_pos, trophy_pos, ghost_pos, player_pos]
        # icons = [None, self.trophy, self.player, self.ghost, self.pipe_texture, self.pipe_texture]
        icons = [self.start, self.pipe_texture, self.pipe_texture, self.trophy, self.ghost, self.player]
        # sizes = [None, 25, 30, 20, 15, 15]
        sizes = [25, 15, 15, 25, 20, 30]
        maze_height = len(self.map)
        maze_width = len(self.map[0])
        wx = round(mapW/maze_width)
        wy = round(mapH/maze_height)

        print(pipe1_pos, pipe2_pos)

        for index, icon in enumerate(icons):
            if icon:
                row, col = positions[index]
                dx, dy = wx*col+wx-10, wy*row 
                #print(index, 576-dy, row)
                self.draw_pic(icon, x=bias_w+dx, y=576-dy, size=sizes[index])

        # self.draw_pic(self.pipe_texture, x=50, y=50, size=50)
        # self.draw_pic(self.ghost, x=80, y=80, size=20)
        # self.draw_pic(self.trophy, x=20, y=30, size=20)
        # self.draw_pic(self.player, x=100, y=100, size=30)


    def wireCube(self, pos):
        glBegin(GL_LINES)
        glColor3f(0, 0, 0)
        bias = 10
        for i in range(max(pos[0]-bias, 0), min(len(self.map), pos[0]+bias)):
            for k in range(max(pos[1]-bias, 0), min(len(self.map[0]), pos[1]+bias)):
                for vertice in cubeVertices:
                    vertice[0]-=i*2
                    vertice[2]-=k*2
                if self.map[i][k] == 1:
                    for cubeEdge in cubeEdges:
                        for cubeVertex in cubeEdge:
                            glVertex3fv(cubeVertices[cubeVertex])
                for vertice in cubeVertices:
                    vertice[0]+=i*2
                    vertice[2]+=k*2
        glEnd()

    def solidCube(self, pos):
        if self.cube is not None:
            glEnable(GL_TEXTURE_2D)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
            # Repeat the texture.
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);

            glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

            glBindTexture(GL_TEXTURE_2D, self.cube)
        glBegin(GL_QUADS)
        # glColor3f(0.8, 0.8, 0.8)
        bias = 7
        for i in range(max(pos[0]-bias, 0), min(len(self.map), pos[0]+bias)):
            for k in range(max(pos[1]-bias, 0), min(len(self.map[0]), pos[1]+bias)):
                for vertice in cubeVertices:
                    vertice[0]-=i*2
                    vertice[2]-=k*2
                if self.map[i][k] == 1:
                    for cubeQuad in cubeQuads:
                        texCount = 0
                        for cubeVertex in cubeQuad:
                            glTexCoord2dv(cubeTextures[texCount])
                            glVertex3fv(cubeVertices[cubeVertex])
                            texCount += 1
                    
                for vertice in cubeVertices:
                    vertice[0]+=i*2
                    vertice[2]+=k*2
        for k in range(len(self.map[0])):
            for i in range(max(pos[0]-1, 0), min(pos[0]+2, len(self.map))):
                for vertice in cubeVertices:
                        vertice[0]-=i*2
                        vertice[2]-=k*2
                if self.map[i][k] == 1:
                    for cubeQuad in cubeQuads:
                        texCount = 0
                        for cubeVertex in cubeQuad:
                            glTexCoord2dv(cubeTextures[texCount])
                            glVertex3fv(cubeVertices[cubeVertex])
                            texCount += 1
                    
                for vertice in cubeVertices:
                    vertice[0]+=i*2
                    vertice[2]+=k*2
        
        for i in range(len(self.map)):
            for k in range(max(0, pos[1]-1), min(pos[1]+2, len(self.map[0]))):
                for vertice in cubeVertices:
                        vertice[0]-=i*2
                        vertice[2]-=k*2
                if self.map[i][k] == 1:
                    for cubeQuad in cubeQuads:
                        texCount = 0
                        for cubeVertex in cubeQuad:
                            glTexCoord2dv(cubeTextures[texCount])
                            glVertex3fv(cubeVertices[cubeVertex])
                            texCount += 1
                    
                for vertice in cubeVertices:
                    vertice[0]+=i*2
                    vertice[2]+=k*2
        glEnd()
        glDisable(GL_TEXTURE_2D)
        # glDeleteTextures([self.texture])
        
    
    def collision_detect(self, x, y, z, angle = None, coordinate = None):
        # b = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        # dis = []
        # for i in b:
        #     if self.map[coordinate[0]+i[0]][coordinate[1]+i[1]] == 1:
        #         dis.append([coordinate[0]+i[0], coordinate[1]+i[1]])
        # print(dis, coordinate, (x, z))
        # dis = np.array(dis, dtype=np.float64)
        # dis *= 2
        # dis -= np.array([x, z], dtype=np.float64)
        # dis = np.sum(dis*dis, axis=1)
        # print(dis)
        # if True in (dis<=2.25):    
        #     return True
        bias = 0.0
        dir = (-bias*math.sin(angle), bias*math.cos(angle))
        # print(x, z, round((x+bias)/2), round((z+bias)/2))
        if round((x+dir[0])/2) >= 0 and round((z+dir[1])/2) >= 0:
            if self.map[round((x+dir[0])/2)][round((z+dir[1])/2)] == 1:
                return True
            elif self.map[round((x+dir[0])/2)][round((z+dir[1])/2)] == 2 and y < 0.2:
                # print(y)
                if (x-round(x/2)*2)**2 + (y-round(y/2)*2)**2 < 0.2:
                    return True
        if x < 0 or z < 0:
            return True
    def on_pipe(self, x, z, y):
        bias = 0.0
        if round((x+bias)/2) >= 0 and round((z+bias)/2) >= 0:
            if self.map[round((x+bias)/2)][round((z+bias)/2)] == 2 and y >= 1:
                print("on pipe", (x, y, z))
                return True

    def get_next_pipe(self, x, z):
        d1 = (self.pipe[0][0]-x)**2 + (self.pipe[0][1]-z)**2
        d2 = (self.pipe[1][0]-x)**2 + (self.pipe[1][1]-z)**2
        if d1 < d2:
            return self.pipe[1]
        else:
            return self.pipe[0]

    def get_pipe(self):
        return self.pipe

    def add_pipe(self, location):
        # dao = 2
        # while dao > 0:
        #     point = (random.randint(0, len(self.map)-1), random.randint(0, len(self.map[0])-1))
        #     if self.map[point[0]][point[1]] == 0:
        #         self.map[point[0]][point[1]] = 2   
        #         dao -= 1
        for i in location:
            print(i)
            self.map[i[1]][i[0]] = 2
