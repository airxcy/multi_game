import numpy as np

class Environment:
	def __init__(self):
		self.scene="none"
		self.walls=[]
	def loadwalls(self,sceneName):
		self.scene=sceneName
		file=open("../crowdData/"+self.scene+".txt","r")
		line = file.readline().strip()
		while line:
			o=np.fromstring(line, dtype=int, sep=',')
			o=np.reshape(o,[-1,2])
			self.walls.append(o)
			line = file.readline().strip()
		file.close()
		print(self.scene+" loaded")


