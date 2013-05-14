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
        self.time = QTime()
        self.timer = QTimer()
        self.x = 0.0
        self.timer.timeout.connect(self.tick)
        

    def initializeGL(self):
        glEnable(GL_TEXTURE_2D)
        glDisable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glEnable(GL_POLYGON_SMOOTH)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glClearColor(0, 0, 0, 1)
        self.loadImages()
        self.time.start()
        self.timer.start(1000/60)

    def paintGL(self):
        self.createPlane()
        
    def loadImages(self):

        # load BackGround Image into Memory
        imageBG = pygame.image.load("Gameplay.jpg")
        imageBGGL = pygame.image.tostring(imageBG, "RGB", 1)

        # load Food images into memory
        foodList = []
        
        image = pygame.image.load("apple.png")
        foodList.append(image)

        image = pygame.image.load("orange.png")
        foodList.append(image)

        image = pygame.image.load("strawberry.png")
        foodList.append(image)

        image = pygame.image.load("snickers.png")
        foodList.append(image)

        image = pygame.image.load("icecreamcone.png")
        foodList.append(image)

        # load textures to videocard
        self.textureBGId = glGenTextures(1)

        glBindTexture(GL_TEXTURE_2D, self.textureBGId)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, imageBG.get_width(), imageBG.get_height(), 0, GL_RGB, GL_UNSIGNED_BYTE, imageBGGL)

        self.textureId = []

        for image in foodList:
            id = glGenTextures(1)
            self.textureId.append(id)
            glImage = pygame.image.tostring(image, "RGBA", 1)

            glBindTexture(GL_TEXTURE_2D, id)
            glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.get_width(), image.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, glImage)

        

    def createPlane(self):
        glClear(GL_COLOR_BUFFER_BIT)

        glEnable( GL_TEXTURE_2D )
        glBindTexture(GL_TEXTURE_2D, self.textureBGId)

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

        glBindTexture(GL_TEXTURE_2D, self.textureId[0])

        glPushMatrix()
        glTranslatef(self.x, 0.0, 0.0)
        glBegin(GL_QUADS)

        glTexCoord2f(0,0)
        glVertex2f(-.1, -.15)

        glTexCoord2f(0,1)
        glVertex2f(-.1, .15)

        glTexCoord2f(1,1)
        glVertex2f(.1, .15)

        glTexCoord2f(1,0)
        glVertex2f(.1, -.15)

        glEnd()
        glPopMatrix()


    def tick(self):
        seconds = self.time.restart() * 0.001

        
        self.update()