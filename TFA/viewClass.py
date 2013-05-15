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

        # Declare and define variables of view class
        self.time = QTime()
        self.timer = QTimer()
        self.x = 0.0
        self.fruitList = []
        self.isTime = 0
        self.kinecttimer = 0

        # generate the kinect runtime environment
        self.kinect = nui.Runtime()

        # enable the skeleton tracking engine on the kinect
        self.kinect.skeleton_engine.enabled = True

        # wait until skeleton is succesfully tracked by kinect before program starts
        Tracked = False
        while not Tracked:
            frame = self.kinect.skeleton_engine.get_next_frame().SkeletonData
            for skeleton in frame:
                if skeleton.eTrackingState == nui.SkeletonTrackingState.TRACKED:
                    self.position = skeleton.SkeletonPositions[JointId.HandRight]
                    Tracked = True
   

        # link timer to Qt for 60 FPS: tick update function will be called
        self.timer.timeout.connect(self.tick)
        

    def initializeGL(self):

        # initializee opengl: function is ran once to prep opengl for program
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
        # draw all opengl to screen

        # paint the BG to screen
        self.createPlane()

        # paint each fruit to the screen
        for fruit in self.fruitList:
            self.drawFruit(fruit.id, fruit.x, fruit.y, fruit.rot)

        # draw the pointer to the screen
        self.drawFruit(self.knifeId, self.position.x, self.position.y, 0)
        
    def loadImages(self):

        # load BackGround Image into Memory
        imageBG = pygame.image.load("Gameplay.jpg")
        imageBGGL = pygame.image.tostring(imageBG, "RGB", 1)

        # load pointer image
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

        # GL COMMANDS TO DRAW QUAD POLYGON: BG
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
        # GL COMMANDS TO DRAW QUAD POLYGON: FRUIT
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

        # HANDLE UPDATE OF SCREEN AND GAME

        # RESTART THE TIMER
        seconds = self.time.restart() * 0.001
        self.isTime += 1
        self.isTime = self.isTime % 60

        # GENREATE NEW FRUIT EVERY FEW SECONDS
        if self.isTime == 0:
            self.fruitList.append(food( self.textureId[int(random.random() * len(self.textureId)-.001)] ))
        
        # CHECK IF CONNECT IS READY TO GIVE NEW FRAME DATA
        if self.kinect.skeleton_frame_ready:



            # DONT GET DATA EVERY FRAME
            if self.kinecttimer == 0:

                # GET SKELETON DATA
                frame = self.kinect.skeleton_engine.get_next_frame().SkeletonData

                for skeleton in frame:
                    if skeleton.eTrackingState == nui.SkeletonTrackingState.TRACKED:

                        # FIND THE POSITION OF THE RIGHT HAND
                        self.position = skeleton.SkeletonPositions[JointId.HandRight]
        self.kinecttimer = (self.kinecttimer + 1)%5
        for fruit in self.fruitList:
            fruit.animate()

            # IF THE FRUIT IS OFF SCREEN DELETE IT
            if fruit.x > 1.1:
                self.fruitList.remove(fruit)

            # CHECK IF HAND IS NEAR FRUIT: IF SO DELETE THE FRUIT
            if abs(fruit.x - self.position.x) < .1 and abs(fruit.y - self.position.y) < .1:
                self.fruitList.remove(fruit)

        # UPDATE THE OPENGL
        self.update()