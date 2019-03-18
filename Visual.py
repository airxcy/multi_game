from simulator import *
from pyglet.gl import *
from labelscene import * 
import numpy as np
from pyglet import image
from pyglet import graphics
from pyglet import sprite
import cv2

warpscale=400
# Direct OpenGL commands to this window.

M=labelsquare(warpscale)
topLeftCoord=trkp = M.dot([0,0,1]).transpose()
topLeftCoord[0]=topLeftCoord[0]/topLeftCoord[2]
topLeftCoord[1]=topLeftCoord[1]/topLeftCoord[2]
class simWindow(pyglet.window.Window):
	def __init__(self, *args, **kwargs):
		#Let all of the arguments pass through
		self.simulator=kwargs['simulator']
		kwargs.pop('simulator', None)
		pyglet.window.Window.__init__(self, *args, **kwargs)
		self.wallList=[]
		for i in range(0,len(self.simulator.scene.walls)):
			numdot=self.simulator.scene.walls[i].shape[0]
			pos=[]
			clr=[]
			for j in range(0,numdot):
				x=self.simulator.scene.walls[i][j][0]
				y=self.simulator.scene.walls[i][j][1]
				pos.extend((x,y))
				clr.extend((255,255,255))
			self.wallList.append(pyglet.graphics.vertex_list(numdot,('v2i', tuple(pos)),('c3B', tuple(clr))))
		self.curPosList=pyglet.graphics.vertex_list(0,('v2i', ()),('c3B', ()))
		self.curRealList=pyglet.graphics.vertex_list(0,('v2i', ()),('c3B', ()))
		self.sceneImg=[]
		self.buffLen=6
		for i in range(0,self.buffLen):
			img = cv2.imread("../crowdData/"+self.simulator.name+"/%06d.jpg"%(i*20))
			warpedImg = cv2.warpPerspective(img,M,(3*warpscale,3*warpscale))
			self.sceneImg.append(image.ImageData(3*warpscale,3*warpscale,'BGR',warpedImg.tostring()))
		self.vhead=0
		self.vtail=3

	def updateScene(self):
		#update Virtal Agent
		l=[]
		clr=[]
		i=0
		for agent in self.simulator.agentQue:
			l.extend((int(agent.state.x),int(agent.state.y)))
			clr.extend((0,255,0))
			i+=1
		#update Real Agent
		for agent in self.simulator.realQue:
			l.extend((int(agent.state.x),int(agent.state.y)))
			clr.extend((255,0,0))
			i+=1
		l.extend((int(topLeftCoord[0]),int(topLeftCoord[1])))
		clr.extend((0,255,255))
		i+=1
		l.extend((int(0),int(0)))
		clr.extend((255,0,255))
		i+=1
		self.curPosList.resize(i)
		self.curPosList.vertices=l
		self.curPosList.colors=clr
		#update Background
		if self.simulator.t%20==0:
			img = cv2.imread("../"+self.simulator.name+"/Frame/%06d.jpg"%(self.simulator.t+60))
			warpedImg = cv2.warpPerspective(img,M,(3*warpscale,3*warpscale))
			self.sceneImg[self.vtail]=image.ImageData(3*warpscale,3*warpscale,'BGR',warpedImg.tostring())
			self.vtail=(self.vtail+1)%self.buffLen
			self.vhead=(self.vhead+1)%self.buffLen	
		self.label = pyglet.text.Label('%d'%(self.simulator.t),
		                          font_name='Times New Roman',
		                          font_size=36,
		                          x=window.width//2, y=window.height//2,
		                          color=(255,255,255,255),
		                          anchor_x='center', anchor_y='center')
	def on_draw(self):
		glClear(GL_COLOR_BUFFER_BIT)
		glClearColor(0.1, 0.5, 0.3, 0.5);
		glLoadIdentity()
		self.sceneImg[self.vhead].blit(0,0)
		for vlist in self.wallList:
			vlist.draw(pyglet.gl.GL_POLYGON)
		self.curPosList.draw(pyglet.gl.GL_POINTS)
		self.label.draw()


simulator= Simulator()
simulator.load("grandCentral")
for i in range(0,10):
	speed = 9+np.random.sample()*2
	angle = 2*np.random.sample()*np.pi
	newAgent = Agent(0,0,0,0,0,0,np.sin(angle)*speed,np.cos(angle)*speed)
	simulator.newEnter(newAgent)
platform = pyglet.window.get_platform()
display = platform.get_default_display()
screens = display.get_screens()
window = simWindow(fullscreen=True, screen=screens[0],simulator=simulator)

simRuning=True
def simUpdate(dt):
	if simRuning:
		simulator.T()
		window.updateScene()


@simWindow.event
def on_key_press(symbol, modifiers):
	simRuning= not simRuning

glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)
glPointSize(10)
glEnable(GL_POINT_SMOOTH)

pyglet.clock.schedule(simUpdate)
pyglet.app.run()
