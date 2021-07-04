from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL.Image import open

class Cube:

    def drawcube(self, texture_id = None, texture_tile = 1.0):

        if texture_id is not None:
            glEnable(GL_TEXTURE_2D)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
            # Repeat the texture.
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);

            glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

            glBindTexture(GL_TEXTURE_2D, texture_id)

        glBegin(GL_QUADS)
        cubeVertices = [[1,1,1],[1,1,-1],[1,-1,-1],[1,-1,1],[-1,1,1],[-1,-1,-1],[-1,-1,1],[-1,1,-1]]
        cubeEdges = ((0,1),(0,3),(0,4),(1,2),(1,7),(2,5),(2,3),(3,6),(4,6),(4,7),(5,6),(5,7))
        cubeQuads = ((0,3,6,4),(2,5,6,3),(1,2,5,7),(1,0,4,7),(7,4,6,5),(2,3,0,1))
        # # Textured cube.
        # glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0,  1.0);
        # glTexCoord2f(texture_tile, 0.0); glVertex3f( 1.0, -1.0,  1.0);
        # glTexCoord2f(texture_tile, texture_tile); glVertex3f( 1.0,  1.0,  1.0);
        # glTexCoord2f(0.0, texture_tile); glVertex3f(-1.0,  1.0,  1.0);
        # glTexCoord2f(texture_tile, 0.0); glVertex3f(-1.0, -1.0, -1.0);
        # glTexCoord2f(texture_tile, texture_tile); glVertex3f(-1.0,  1.0, -1.0);
        # glTexCoord2f(0.0, texture_tile); glVertex3f( 1.0,  1.0, -1.0);
        # glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0, -1.0);
        # glTexCoord2f(0.0, texture_tile); glVertex3f(-1.0,  1.0, -1.0);
        # glTexCoord2f(0.0, 0.0); glVertex3f(-1.0,  1.0,  1.0);
        # glTexCoord2f(texture_tile, 0.0); glVertex3f( 1.0,  1.0,  1.0);
        # glTexCoord2f(texture_tile, texture_tile); glVertex3f( 1.0,  1.0, -1.0);
        # glTexCoord2f(texture_tile, texture_tile); glVertex3f(-1.0, -1.0, -1.0);
        # glTexCoord2f(0.0, texture_tile); glVertex3f( 1.0, -1.0, -1.0);
        # glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0,  1.0);
        # glTexCoord2f(texture_tile, 0.0); glVertex3f(-1.0, -1.0,  1.0);
        # glTexCoord2f(texture_tile, 0.0); glVertex3f( 1.0, -1.0, -1.0);
        # glTexCoord2f(texture_tile, texture_tile); glVertex3f( 1.0,  1.0, -1.0);
        # glTexCoord2f(0.0, texture_tile); glVertex3f( 1.0,  1.0,  1.0);
        # glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0,  1.0);
        # glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0, -1.0);
        # glTexCoord2f(texture_tile, 0.0); glVertex3f(-1.0, -1.0,  1.0);
        # glTexCoord2f(texture_tile, texture_tile); glVertex3f(-1.0,  1.0,  1.0);
        # glTexCoord2f(0.0, texture_tile); glVertex3f(-1.0,  1.0, -1.0);
        for cubeQuad in cubeQuads:
            for cubeVertex in cubeQuad:
                glVertex3fv(cubeVertices[cubeVertex])
        # Colored cube.
        #
        # glColor3f(1.0, 0.5, 0.0)
        # glVertex3f( 1.0, 1.0, 1.0)
        # glVertex3f(-1.0, 1.0, 1.0)
        # glVertex3f(-1.0,-1.0, 1.0)
        # glVertex3f( 1.0,-1.0, 1.0)
        
        # glColor3f(1.0, 0.0, 0.5)
        # glVertex3f( 1.0,-1.0,-1.0)
        # glVertex3f(-1.0,-1.0,-1.0)
        # glVertex3f(-1.0, 1.0,-1.0)
        # glVertex3f( 1.0, 1.0,-1.0)
        
        # glColor3f(0.0, 1.0, 0.5)
        # glVertex3f(-1.0, 1.0, 1.0)
        # glVertex3f(-1.0, 1.0,-1.0)
        # glVertex3f(-1.0,-1.0,-1.0)
        # glVertex3f(-1.0,-1.0, 1.0)
        
        # glColor3f(0.5, 0.0, 1.0)
        # glVertex3f(1.0, 1.0,-1.0)
        # glVertex3f(1.0, 1.0, 1.0)
        # glVertex3f(1.0,-1.0, 1.0)
        # glVertex3f(1.0,-1.0,-1.0)

        glEnd()
