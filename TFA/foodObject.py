class food():
    def __init__ (self, _x0, _y0, _r0, _rotSpeed, _id ):
    	self.x0 = _x0
    	self.y0 = _y0
    	self.r0 = _r0
    	self.rotSpeed = _rotSpeed
    	self.id = _id
    	self.speed = .017

    def animate(self):
    	self.x += self.speed
    	self.y  = -(self.x - self.x0)(self.x-self.x0) + y0

    def setRand(self):
    	self.x = -1
    	self.y = -1

    







