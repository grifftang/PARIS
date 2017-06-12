import pyglet, os

class Stimulus(object):
	def __init__(self,name,path):
		self.render = pyglet.resource.image(path)
		self.position = "left"
		self.xPos = 150
		self.yPos = 200
		self.path = path
		self.times = []

	def posUpdate(self,symbol):
		if symbol == 119: self.yPos += 10
		elif symbol == 97: self.xPos -= 10
		elif symbol == 115: self.yPos -= 10
		elif symbol == 100: self.xPos += 10

	def recordEntry(self,name,position,time):
		time = round(time,3)
		self.times.append((name,position,time))

	def draw(self):
		self.render.blit(self.xPos,self.yPos)