import pygame as pg
from pygame.locals import *
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *
from objloader import *

cubeVertices = [[1,1,1],[1,1,-1],[1,-1,-1],[1,-1,1],[-1,1,1],[-1,-1,-1],[-1,-1,1],[-1,1,-1]]
cubeTextures = [[0, 0], [0, 1], [1, 1], [1, 0]]
cubeEdges = ((0,1),(0,3),(0,4),(1,2),(1,7),(2,5),(2,3),(3,6),(4,6),(4,7),(5,6),(5,7))
cubeQuads = ((0,3,6,4),(2,5,6,3),(1,2,5,7),(1,0,4,7),(7,4,6,5),(2,3,0,1))

class maze:
    def __init__(self, map, texture_id = None):
        self.map = map
        self.texture = texture_id
    def wireCube(self):
        glBegin(GL_LINES)
        glColor3f(0.5, 1.0, 1.0)
        for i in range(len(self.map)):
            for k in range(len(self.map[0])):
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

    def solidCube(self):
        if self.texture is not None:
            glEnable(GL_TEXTURE_2D)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
            # Repeat the texture.
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);

            glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

            glBindTexture(GL_TEXTURE_2D, self.texture)
        glBegin(GL_QUADS)
        glColor3f(0.5, 1.0, 1.0)
        for i in range(len(self.map)):
            for k in range(len(self.map[0])):
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
    
    def collision_detect(self, x, z):
        bias = 0.0
        # print(x, z, round((x+bias)/2), round((z+bias)/2))
        if round((x+bias)/2) >= 0 and round((z+bias)/2) >= 0:
            if self.map[round((x+bias)/2)][round((z+bias)/2)] == 1:
                return True