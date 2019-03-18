import numpy as np
num_direction=1024
class agentState:
	def __init__(self):
		self.x=0
		self.y=0
		self.desx=0
		self.desy=0
		self.prefSpd=0
		self.id=0
class Action:
	def __init__(self,vx,vy):
		self.vx=vx
		self.vy=vy
class Agent():
	def __init__(self,i,x,y,desx,desy,prefSpd,vx,vy):
		self.observation=0
		self.model=0
		self.id=i
		self.state=agentState()
		self.state.x=x
		self.state.y=y
		self.state.desx=desx
		self.state.desy=desy
		self.state.prefSpd=prefSpd
		self.action=Action(vx,vy)
	def updateStates(self,newState):
		self.state=newState
	def moveTo(self,x,y):
		self.action.vx=x-self.state.x
		self.action.vy=y-self.state.y
		self.state.x=x
		self.state.y=y
	def movePolicy(self,dx,dy):
		self.action.vx=dx
		self.action.vy=dy
		self.state.x+=dx
		self.state.y+=dy
	def updateObservation(self,newObervation):
		self.observation=newObervation
	def	policy(self):
		return self.action

class Human:
	def loadFromFile(self):
		print("loading...")
	def initFromTrk(self,trk,i):
		self.trk=trk
		self.life=trk.shape[0]
		self.born=trk[0,2]
		self.die=trk[self.life-1,2]
		self.age=0
		self.id=i
		self.srcx=trk[0,0]
		self.srcy=trk[0,1]
		self.desx=trk[self.life-1,0]
		self.desy=trk[self.life-1,1]
		self.prefSpd=0
		self.observations=np.zeros((self.life,num_direction*3+3),dtype=float)
		x=self.desx-self.srcx
		y=self.desy-self.srcy
		d=np.sqrt(x*x+y*y)
		self.dirx=x/d
		self.diry=y/d
		x=self.trk[1,0]-self.trk[0,0]
		y=self.trk[1,1]-self.trk[0,1]
		d=np.sqrt(x*x+y*y)
		if d>0:
			self.dirx=x/d
			self.diry=y/d
	def getLoc(self):
		reutrn (self.trk[self.age,0],self.trk[self.age,1])

