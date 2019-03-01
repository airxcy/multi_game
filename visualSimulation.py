import cv2
from simulator import *
from VAgent import *

simulator=Simulator()
simulator.load("grandCentral")
bg=np.zeros([simulator.worldlimit,simulator.worldlimit,3])
for i in range(0,len(simulator.scene.walls)):
	numdot=simulator.scene.walls[i].shape[0]
	for j in range(1,numdot+1):
		i0=(j-1)%numdot
		i1=j%numdot
		x_0=simulator.scene.walls[i][i0][0]
		y_0=simulator.scene.walls[i][i0][1]
		x_1=simulator.scene.walls[i][i1][0]
		y_1=simulator.scene.walls[i][i1][1]
		cv2.line(bg,(x_0,y_0),(x_1,y_1),(0,0,255),2)
ckey=0
for i in range(0,10):
	speed = 9+np.random.sample()*2
	angle = 2*np.random.sample()*np.pi
	newAgent = Agent(0,0,0,0,0,np.sin(angle)*speed,np.cos(angle)*speed)
	print(np.sin(angle)*speed,np.cos(angle)*speed)
	simulator.newEnter(newAgent)

