from environment import *
from Agent import *
import os


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
		self.Ndir=64
		self.radDiv=2*np.pi/self.Ndir
	def load(self,name):
		self.name=name
		self.scene.loadwalls(name)
		dirpath="Data/"+name+"_%02d_%d"%(timeStep,num_direction)
		if os.path.isdir(dirpath):
			print("load path:"+dirpath)
		else:
			data=np.load("scene/"+name+".npz")
			os.mkdir(dirpath)
			trks=data['trks']
			Ids=data['ids']
			self.numtrk=self.realTrk.shape[0]
			self.activeRecords=np.array(list(range(0,self.numtrk)))
			i=0
			for trk in trks:
				newHuman = Human()
				newHuman.initFromTrk(trk,i)
				self.npc.append(newHuman)
				i+=1
			self.mortals=np.empty((0), dtype=Agent)
	def newEnter(self,newAgents):
		self.agentQue=np.append(self.agentQue,newAgents)
	def disappear(self,idxset):
		self.agentQue=np.delete(self.agentQue,idxset)
	def T(self):
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

		# 	txtcoord=txtcoord+str(agent.state.x)+","+str(agent.state.y)+","
		#	print(txtcoord)
	def T_real(self):
		for human in self.npc:
			if self.t==human.born:
				self.mortals=np.append(self.mortals,human.id)
		carnage=np.empty((0), dtype=int)
		for i in self.mortals:
			human = self.npc[i]
			human.age=self.t-human.born
			if human.age>=human.life:
				carnage=np.append(carnage,i)
		self.mortals=np.delete(self.mortals,carnage)
		for i in self.mortals:
			for obstacles in range(0,self.scene.walls):
				for radi in range(0,self.Ndir):
					rad = self.radDiv*(radi-self.Ndir/2+1)
					dx,dy=angleVec(dirvec,rad)
					for k in range(0,int(obstacles.stacklen[j])):
						a=obstacles.polystack[j,k,:]
						b=obstacles.polystack[j,(k+1)%int(obstacles.stacklen[j]),:]
						xab=a[0]-b[0]
						yab=a[1]-b[1]
						lineangle = (yab*dx-dy*xab)
						if abs(lineangle)>0.0000001:
							crossx=((ci[1]-a[1])*dx*xab-dy*ci[0]*xab+yab*a[0]*dx)/lineangle
							if abs(dx)>0:
								crossy=dy/dx*(crossx-ci[0])+ci[1]
							else:
								crossy=yab/xab*(crossx-a[0])+a[1]
							if abs(xab)>0:
								t2=(crossx-b[0])/xab
							else:
								t2=(crossy-b[1])/yab
							if abs(dx)>0:
								t1=(crossx-ci[0])/dx
							else:
								t1=(crossy-ci[1])/dy
							if t2>=0 and t2<=1 and t1>=0:
								if depthVec[curi,radi]<0 or depthVec[curi,radi]>t1:
									depthVec[curi,radi]=t1
		added=[]
		addeidx=0
		for i in self.activeRecords:
			trki = self.realTrk[i]
			startifidx=int(trki[0,2])
			endfidx=trki[trki.shape[0]-1,2]
			if startifidx==self.t:
				x=trki[0,0]
				y=trki[0,1]
				x1=trki[19,0]
				y1=trki[19,1]
				dx=x1-x
				dy=y1-y
				dirlen = np.sqrt(dx*dx+dy*dy)
				desx=trki[trki.shape[0]-1,0]
				desy=trki[trki.shape[0]-1,1]
				newAgent = Agent(i,x,y,desx,desy,dirlen,dx,dy)
				newAgent.observation=

				self.realQue=np.append(self.realQue,newAgent)
				added.append(addeidx)

			addeidx+=1
		self.activeRecords=np.delete(self.activeRecords,added)
		for agent in self.realQue:

	def scanDepth(self,dirvec,depthvec):
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

