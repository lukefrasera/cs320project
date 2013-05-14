from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtOpenGL import *
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import math

class view(QGLWidget):
    def __init__(self):
        super(view, self).__init__()

    def initializeGL(self):
        glEnable(GL_TEXTURE_2D)
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_COLOR_MATERIAL)
        glEnable(GL_BLEND)
        glEnable(GL_POLYGON_SMOOTH)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glClearColor(0, 0, 0, 1)
        self.loadImages()

    def paintGL(self):
        self.createPlane()
        
    def loadImages(self):
        image = pygame.image.load("image.JPG")
        imageGl = pygame.image.tostring(image, "RGB", 1)

        self.textureId = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.textureId)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.get_width(), image.get_height(), 0, GL_RGB, GL_UNSIGNED_BYTE, imageGl)

        

    def createPlane(self):
        glClear(GL_COLOR_BUFFER_BIT)

        glEnable( GL_TEXTURE_2D )
        glBindTexture(GL_TEXTURE_2D, self.textureId)

        glBegin(GL_QUADS)

        glTexCoord2f(0,0)
        glVertex2f(-1, -1)

        glTexCoord2f(0,1)
        glVertex2f(-1, 1)

        glTexCoord2f(1,1)
        glVertex2f(1, 1)

        glTexCoord2f(1,0)
        glVertex2f(1, -1)

        glEnd()