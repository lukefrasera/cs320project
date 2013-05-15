from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtOpenGL import *
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

from foodObject import food

import math
import random
import thread
import itertools
import ctypes
import pykinect
from pykinect import nui
from pykinect.nui import JointId

class view(QGLWidget):
    def __init__(self):
        super(view, self).__init__()
        self.time = QTime()
        self.timer = QTimer()
        self.x = 0.0
        self.fruitList = []
        self.isTime = 0
        self.kinecttimer = 0

        self.RIGHT_ARM = (JointId.ShoulderCenter, 
             JointId.ShoulderRight, 
             JointId.ElbowRight, 
             JointId.WristRight, 
             JointId.HandRight)


        self.kinect = nui.Runtime()
        self.kinect.skeleton_engine.enabled = True

        
        Tracked = False
        while not Tracked:
            frame = self.kinect.skeleton_engine.get_next_frame().SkeletonData
            for skeleton in frame:
                if skeleton.eTrackingState == nui.SkeletonTrackingState.TRACKED:
                    self.position = skeleton.SkeletonPositions[JointId.HandRight]
                    Tracked = True
   

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

        for fruit in self.fruitList:
            self.drawFruit(fruit.id, fruit.x, fruit.y, fruit.rot)

        self.drawFruit(self.knifeId, self.position.x, self.position.y, 0)
        
    def loadImages(self):

        # load BackGround Image into Memory
        imageBG = pygame.image.load("Gameplay.jpg")
        imageBGGL = pygame.image.tostring(imageBG, "RGB", 1)

        kimage = pygame.image.load("knife.png")
        kimageGL = pygame.image.tostring(kimage, "RGBA", 1)

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

        self.knifeId = glGenTextures(1)

        glBindTexture(GL_TEXTURE_2D, self.knifeId)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, kimage.get_width(), kimage.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, kimageGL)

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
    
    def drawFruit(self, id, x, y, r):
        glBindTexture(GL_TEXTURE_2D, id)
        glPushMatrix()

        glTranslatef(x, y, 0.0)
        glRotatef(r, 0, 0, 1)

        glBegin(GL_QUADS)

        glTexCoord2f(0,0)
        glVertex2f(-.1, -.1)

        glTexCoord2f(0,1)
        glVertex2f(-.1, .1)

        glTexCoord2f(1,1)
        glVertex2f(.1, .1)

        glTexCoord2f(1,0)
        glVertex2f(.1, -.1)

        glEnd()

        glPopMatrix()


    def tick(self):
        seconds = self.time.restart() * 0.001
        self.isTime += 1
        self.isTime = self.isTime % 60

        if self.isTime == 0:
            self.fruitList.append(food( self.textureId[int(random.random() * len(self.textureId)-.001)] ))
        
        if self.kinect.skeleton_frame_ready:



            
            if self.kinecttimer == 0:
                frame = self.kinect.skeleton_engine.get_next_frame().SkeletonData

                for skeleton in frame:
                    if skeleton.eTrackingState == nui.SkeletonTrackingState.TRACKED:
                        self.position = skeleton.SkeletonPositions[JointId.HandRight]
        self.kinecttimer = (self.kinecttimer + 1)%5
        for fruit in self.fruitList:
            fruit.animate()

            if fruit.x > 1.1:
                self.fruitList.remove(fruit)
            if abs(fruit.x - self.position.x) < .1 and abs(fruit.y - self.position.y) < .1:
                self.fruitList.remove(fruit)
        self.update()