from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL.Image import open, ROTATE_90
import numpy

class Texture:

    def loadImage(self, filename, type="jpg", angle = 0):
        try:
            image = open(filename)
        except IOError as ex:
            print('IOError: failed to open texture file')
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            return -1
        image = image.rotate(angle)
        # image.show()
        # print('Opened image file: size =', image.size, 'format =', image.format)
        imageData = numpy.array(list(image.getdata()), numpy.uint8)
        # print(imageData, numpy.array(image.getdata()))

        textureID = glGenTextures(1)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 4)
        glBindTexture(GL_TEXTURE_2D, textureID)
        if type == "jpg":
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_BASE_LEVEL, 0)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAX_LEVEL, 0)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.size[0], image.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, imageData)
        if type == "png":
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.size[0], image.size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, imageData)
        image.close()

        return textureID
