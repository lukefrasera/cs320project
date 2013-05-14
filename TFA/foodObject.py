import random

class food():
    def __init__ (self, _id ):
    	self.id = _id
        self.genRandFunc()

    def animate(self):
    	self.x += self.speed
        self.rot += self.rotspeed
        self.rot = self.rot % 360

    	self.y  = -(self.x - self.x0) * (self.x-self.x0) + self.y0

    def setRand(self):
    	self.x = -1
    	self.y = -1

    def genRandFunc(self):
        self.y0 = random.random() * 1.3 - .5
        self.x0 = random.random() * 1.6 - .8
        self.a0 = random.random() * 5
        self.x = -1
        self.speed = 0.017
        self.rotspeed = (random.random()*2-1) * 15
        self.rot = random.random() * 360







