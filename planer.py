import numpy as np
import datetime
from collections import OrderedDict

class Node:
	def __init__(self,name,value=None):
		self.name=name
		self.value=value
	def hasValue(self):
			if self.value is None:
				return False
			else:
				return True
	def getValue(self,mode=0):
			if self.value is None:
				return None
			else:
				return (self.value[0],self.value[1])
class Edge:
	def __init__(self,n1,n2,weight=1):
		self.n1=n1
		self.n2=n2
		self.weight=weight

class Graph:
	def __init__(self):
		self.V=OrderedDict()
		self.E=OrderedDict()
	def addV(self,name,v=None):
		n=Node(name,v)
		self.V[name]=n
		return n

	def addE(self,n1,n2,w=1):
		ekey=n1.name+n2.name
		self.E[ekey]=Edge(n1,n2,w)

class Tree(Graph):
	def __init__(self):
		Graph.__init__(self)
	def _addChild(self,parent,child,v=None,w=1):
		if bool(self.V):
			n1=self.V[parent]
			n2=self.addV(child,v)
			self.addE(n1,n2,w)
			self.children[parent].append(child)
			self.childrenIdx[parent][child]=len(self.childrenIdx[parent])
			self.parents[child]=parent
			self.children[child]=[]
			self.childrenIdx[child]={}
		else:
			n2=self.addV(child,v)
			self.parents={child:None}
			self.children={child:[]}
			self.childrenIdx={child:{}}
			self.root=child


class ResearchTree(Tree):
	def __init__(self,name):
		Tree.__init__(self)
		self.instanceCost={}
		self.pastTime={}
		self.finishDate={}
		self.skipeddays={}
		self.sbling={name:None}
		self.addChild(None,name)

	def getSbling(self,n):
		if n and self.parents[n] and self.childrenIdx[self.parents[n]][n]>0:
			numSbling = self.childrenIdx[self.parents[n]][n]-1
			return self.children[self.parents[n]][numSbling]
		elif n:
			return self.getSbling(self.parents[n])
		return n

	def addChild(self,parent,child,v=None,w=1):
		self._addChild(parent,child,v,w)
		self.pastTime[child]=0
		self.finishDate[child]=0
		self.skipeddays[child]=0
		self.sbling[child]=self.getSbling(child)

	def hello(self,name,depth=0):
		if self.children[name]:
			for child in self.children[name]:
				self.hello(child,depth+1)
		line=""
		for i in range(0,depth):
			line+="| "
		line=line+"|-"+name
		line = "{:<100}".format(line)
		if self.V[name].getValue() is None:
			line=line+"|"
		else:
			line=line+"|"+"min:"+str(self.V[name].value[0])+",max:"+str(self.V[name].value[1])
		print(line)

	def calTime(self,task,startDate,mode=0,depth=0):
		timePast=0
		workedDays=0
		realDays=0
		instanceCost=0
		skiped=0
		costTime=0
		self.pastTime[task]=timePast
		if self.children[task]:
			for child in self.children[task]:
				timeCost,startDate=self.calTime(child,startDate,mode,depth+1)
				timePast+=timeCost
		else:
			if task=="Contingency":
				costTime = int(self.pastTime[self.sbling[task]]*0.1)
			else:
				costTime = self.V[task].value[mode]
			while workedDays<costTime:
				date=startDate+ datetime.timedelta(days=realDays)
				weekday = date.weekday()
				if weekday in [0,1,3,4]:
					workedDays+=1
				else:
					skiped+=1
				realDays+=1
			timePast=realDays
			startDate = startDate+datetime.timedelta(days=timePast)
		if realDays>0:
			instanceCost=realDays
		else:
			instanceCost=None
		if self.sbling[task]:
			self.pastTime[task]=self.pastTime[self.sbling[task]]+timePast
		else:
			self.pastTime[task]=timePast

		

		line=""
		for i in range(0,depth):
			line+="| "
		line = line+"|-"+task
		line = "{:<40}".format(line)+"|"+(str(self.V[task].getValue()) if self.V[task].getValue() else "")
		line = "{:<50}".format(line)+"|"+(str(instanceCost) if instanceCost else "")
		line = "{:<70}".format(line)+"|"+(str(self.pastTime[task]) if self.pastTime[task] else "")
		line = "{:<90}".format(line)+"|"+(str(startDate.date()) if startDate else "")
		line = "{:<110}".format(line)+"|"+(str(skiped) if skiped else "")
		line = "{:<120}".format(line)+"|"+("Level %d Progress Meetings"%(depth) if (depth<3 and mode and not task=="Contingency")  else "")
		print(line)
		return (timePast,startDate)


	def evaluateTime(self,startDate):
		line = "|Task Tree"
		line = "{:<40}".format(line)+"|estimate"
		line = "{:<50}".format(line)+"|instance cost"
		line = "{:<70}".format(line)+"|cumulate cost"
		line = "{:<90}".format(line)+"|finish Date"
		line = "{:<110}".format(line)+"|skiped"
		line = "{:<120}".format(line)+"|Possible Meetings"
		print("#################### Best Case(Start:"+str(startDate.date())+") #################")
		print(line)
		minCost,earlest=self.calTime(self.root,startDate)
		print("#################### Worst Case(Start:"+str(startDate.date())+") #################")
		print(line)
		maxCost,latest=self.calTime(self.root,startDate,1)
		print("minimum Cost Days:%d, maximum cost days:%d"%(minCost,maxCost))
		return (earlest,latest)

class graphicsConference(ResearchTree):
	def __init__(self,name):
		ResearchTree.__init__(self,name)
		self.addChild(self.root,"Data")
		self.addChild(self.root,"Method")
		self.addChild(self.root,"Experiments")
		self.addChild(self.root,"Conference Writing",np.array([20,30]))
		self.addChild(self.root,"Contingency",np.array([0,0]))

		self.addChild("Data","grandCentral",np.array([2,3]))
		self.addChild("Data","dataset2",np.array([2,3]))
		self.addChild("Data","dataset3",np.array([2,3]))
		self.addChild("Method","Simulator")
		self.addChild("Method","Visualizer",np.array([1,2]))
		self.addChild("Simulator","Agents")
		self.addChild("Simulator","Other MDP components",np.array([0,1]))
		self.AgentSetup()
		self.addChild("Experiments","Self Comparison",np.array([12,14]))
		self.addChild("Experiments","Peer Comparison")
		self.addChild("Peer Comparison","Social LSTM",np.array([12,18]))
		self.addChild("Peer Comparison","Social GAN",np.array([12,18]))
		self.addChild("Peer Comparison","Classical")
		self.addChild("Classical","Menge",np.array([12,18]))
		self.addChild("Classical","SceneGeneration",np.array([6,8]))
		self.addChild("Peer Comparison","Guy Siggraph Asia 2012",np.array([12,18]))

	def AgentSetup(self):
		self.addChild("Agents","Behaviour Cloning",np.array([5,7]))
		self.addChild("Agents","GAIL")
		self.addChild("GAIL","Environment Set up",np.array([5,7]))
		self.addChild("GAIL","Implementation coding",np.array([2,3]))
		self.addChild("GAIL","Implementation Validation",np.array([4,7]))
		self.addChild("Agents","GAIL++")
		self.addChild("GAIL++","Solving Mode Collapsing",np.array([9,15]))
		self.addChild("GAIL++","Mode Clustering",np.array([9,15]))


class Thesis(ResearchTree):
	def __init__(self,name):
		ResearchTree.__init__(self,name)
		self.addChild(self.root,"First Draft")
		self.addChild(self.root,"Second Draft")
		self.addChild(self.root,"Final Round")
		self.addChild(self.root,"Contingency",np.array([0,0]))
		self.addChild("Second Draft","Editors Reading",np.array([10,15]))
		self.addChild("Second Draft","Editing",np.array([8,12]))
		self.addChild("Final Round","Editors Reading",np.array([7,10]))
		self.addChild("Final Round","Editing",np.array([5,6]))
		self.addChild("First Draft","Introduction")
		self.addChild("Introduction","Contribution",np.array([1,2]))
		self.addChild("Introduction","Thesis Overview",np.array([1,2]))
		self.addChild("First Draft","Preliminaries")
		self.addChild("Preliminaries","Crowd",np.array([1,2]))
		self.addChild("Preliminaries","Robotics",np.array([1,2]))
		self.addChild("Preliminaries","Reinfocement Learning ",np.array([1,2]))
		self.addChild("Preliminaries","Inverse Reinfocement Learning ",np.array([1,2]))
		self.addChild("Preliminaries","Generative Models",np.array([1,2]))

		self.addChild("First Draft","Data")
		self.addChild("Data","First Person View",np.array([1,2]))
		self.addChild("Data","Third Person View",np.array([1,2]))
		self.addChild("Data","Data Processing",np.array([1,2]))

		self.addChild("First Draft","Model")
		self.addChild("Model","Behaviour Cloning")
		self.addChild("Model","Generative Adverserial Imitation Learning")
		self.addChild("Model","Decentralized GAIL")
		self.addChild("Behaviour Cloning","Theory",np.array([1,2]))
		self.addChild("Behaviour Cloning","Implementation",np.array([1,2]))
		self.addChild("Generative Adverserial Imitation Learning","Theory",np.array([1,2]))
		self.addChild("Generative Adverserial Imitation Learning","Implementation",np.array([1,2]))
		self.addChild("Decentralized GAIL","Theory",np.array([1,2]))
		self.addChild("Decentralized GAIL","Implementation",np.array([1,2]))

		self.addChild("First Draft","Experiments")
		self.addChild("Experiments","Simulations",np.array([1,2]))
		self.addChild("Experiments","Predictions",np.array([1,2]))
		self.addChild("Experiments","Representations",np.array([1,2]))
		
		self.addChild("First Draft","Evalutions")
		self.addChild("Evalutions","metrics",np.array([1,2]))
		self.addChild("Evalutions","frameworks",np.array([1,2]))
		self.addChild("Evalutions","Analysis & Comparisons",np.array([1,2]))

		self.addChild("First Draft","Conclusions")
		self.addChild("Conclusions","Thesis Contributions",np.array([1,2]))
		self.addChild("Conclusions","Future Directions",np.array([1,2]))
		self.addChild("First Draft","Acknowledgement,Formats,Wording, etc",np.array([1,2]))

thesis=Thesis("A ph.D Thesis")


paper=graphicsConference("A Graphics Paper")
earlist,latest=paper.evaluateTime(datetime.datetime.now())
earlist,latest=thesis.evaluateTime(latest)
		# self.addChild("Thesis","First Draft")
		# self.addChild("First Draft","Introduction",np.array([1,2]))
		# self.addChild("First Draft","Preliminaries",np.array([5,6]))

# simVisualizer={"simulation Visualizer",simulator,np.array([2,3])}
# sceneUpdater={"observation":np.array([2,3])}
# Agents={
# "Behaviour Cloning":np.array([5,8]),
# "GAIL":
# }
# Simulator=DataProcessor+Visualizeer+Agents+Environments+sceneUpdater
