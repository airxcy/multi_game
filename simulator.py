from environment import *
from Agent import *
from trigonometry import *
import os
num_direction=64
radDiv=2*np.pi/num_direction
class Simulator():
	def __init__(self):
		self.agentQue=np.empty((0), dtype=Agent)
		self.worldlimit=400*3
		self.scene = Environment()
		self.npc=[]
		self.numtrk=800
		self.t=0
		self.realTrk=[]
		self.realIds=[]
		self.name=0

		self.timeStep=20
	def load(self,name):
		self.name=name
		self.scene.loadwalls(name)
		dirpath="D:/crowdData/"+name+"_%02d_%d"%(self.timeStep,num_direction)
		if os.path.isdir(dirpath):
			print("load path:"+dirpath)
		else:
			os.mkdir(dirpath)
		data=np.load("D:/crowdData/"+name+"/trk_ids.npz")
		self.realTrk=data['trks']
		self.realIds=data['ids']
		self.numtrk=self.realTrk.shape[0]
		self.mortals=np.array(list(range(0,self.numtrk)))
		i=0
		for trk in self.realTrk:
			if trk.shape[0]>1:
				newHuman = Human()
				newHuman.initFromTrk(trk[0::self.timeStep],i,num_direction)
				self.npc.append(newHuman)
				i+=1
		# trks=
		self.mortals=np.empty((0), dtype=int)
	def newEnter(self,newAgents):
		self.agentQue=np.append(self.agentQue,newAgents)
	def disappear(self,idxset):
		self.agentQue=np.delete(self.agentQue,idxset)
	def T(self):
		if self.t%self.timeStep==0:
			self.T_real()
		for agent in self.agentQue:
			action = agent.policy()
			newStates=agentState()
			newStates.x+=agent.state.x+agent.action.vx
			newStates.y+=agent.state.y+agent.action.vy
			newStates.desx=agent.state.desx
			newStates.desy=agent.state.desy
			newStates.prefSpd=agent.state.prefSpd
			agent.updateStates(newStates)
		self.t+=1
	def T_real(self):
		for human in self.npc:
			if self.t==human.born:
				self.mortals=np.append(self.mortals,human.id)
		carnage=[]
		i_pos=0
		for i in self.mortals:
			human = self.npc[i]
			human.age=human.age+1
			if human.age>=human.life:
				carnage.append(i_pos)
			i_pos=i_pos+1
		self.mortals=np.delete(self.mortals,carnage)
		# TODO calculate depth 
		self.updateDepthSensor()

	def updateDepthSensor(self):
		for i in self.mortals:
			human = self.npc[i]		
			#https://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect
			for radi in range(0,num_direction):
				rad = radDiv*(radi-num_direction/2+1)
				xc,yc=human.getLoc()
				dirx,diry=human.getDir()
				xr,yr=angleVec(dirx,diry,rad)
				depthVal=-1
				for wall in self.scene.walls:
					numdot=wall.shape[0]
					for j in range(0,numdot):
						a=wall[j,:]
						j1=(j+1)%numdot
						b=wall[j1,:]
						xa=a[0]
						ya=a[1]
						xb=b[0]
						yb=b[1]
						denominator = ((xb-xa)*yr-(yb-ya)*xr)
						if abs(denominator)>0.0000001:
							lmda=((ya-yc)*xr-(xa-xc)*yr)/denominator
							t=((xc-xa)*(yb-ya)-(yc-ya)*(xb-xa))/denominator
							if lmda>0 and lmda<1 and t>0 and (depthVal<0 or depthVal>t):
								# print(lmda,t)
								depthVal=t
				for hid in self.mortals:
					if hid!=i:
						pedestrain = self.npc[hid]
						xp,yp=pedestrain.getLoc()
						dx=xp-xc
						dy=yp-yc
						dist=np.sqrt(dx*dx+dy*dy)
						if dist>0:
							if depthVal<0 or dist<depthVal:
								blockwidth=np.pi/(dist+1)
								sign, centerRad=vec2Angle(dx/dist,dy/dist,dirx,diry)
								if rad>sign*centerRad-blockwidth and rad<sign*centerRad+blockwidth:
									depthVal=dist
						else:
							depthVal=dist
				human.observations[human.age,radi]=depthVal
	def visualScan(self,agent,depthvec,velovec):
		cx=agent.x
		cy=agent.y
		vx=agent.action.vx
		vy=agent.action.vy
		dirlen = math.sqrt(vx*vx+vy*vy)
		if dirlen<=0:
			angle = 2*np.random.sample()*np.pi
			dirvec=[np.cos(angle),np.sin(angle)]
		else:
			dirvec=[vx/dirlen,vy/dirlen]
		self.scanDepth(dirvec,depthvec)
