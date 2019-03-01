import cv2
import numpy as np
import os, os.path
curidx=0
curpos = np.zeros([2],dtype=int)
bbox = np.zeros([4,2],dtype=int)

def draw_square(event,x,y,flags,param):
	global curidx
	if event == cv2.EVENT_MOUSEMOVE:
		curpos[0]=x
		curpos[1]=y
	if event == cv2.EVENT_LBUTTONDBLCLK:
		if curidx<4:
			bbox[curidx,0]=x
			bbox[curidx,1]=y
			curidx=curidx+1

def labelsquare(warpscale):
	# img = cv2.imread("Frame/000020.jpg")
	# drawImg=img.copy()
	# # curidx=0
	
	# # label square
	# cv2.namedWindow('image',cv2.WINDOW_NORMAL)
	# cv2.setMouseCallback('image',draw_square)
	# while(1):
	# 	drawImg=img.copy()
	# 	for i in range(0,curidx):
	# 		cv2.circle(drawImg,(bbox[i,0],bbox[i,1]),5,(0,0,255),-1)
	# 		if i>0:
	# 			cv2.line(drawImg,(bbox[i-1,0],bbox[i-1,1]),(bbox[i,0],bbox[i,1]),(0,0,255),1)
	# 	if curidx>0:
	# 		cv2.line(drawImg,(curpos[0],curpos[1]),(bbox[curidx-1,0],bbox[curidx-1,1]),(0,0,255),1)
	# 	cv2.imshow('image',drawImg)
	# 	cv2.waitKey(20)
	# 	if curidx==4:
	# 		break
	# pts=np.float32(bbox)
	pts=np.float32([[  441.,178.],[ 1446.,189.],[ 1784.,800.],[  148.,794.]]) #Grand Central
	normsquar=np.float32([[warpscale,warpscale],[2*warpscale,warpscale],[2*warpscale,2*warpscale],[warpscale,2*warpscale]])
	M = cv2.getPerspectiveTransform(pts,normsquar)
	return M


class Obstacle:
	def __init__(self):
		self.stackidx=0
		self.stacklen=np.zeros([20,1],dtype=int)
		self.polystack=np.zeros([20,20,2],dtype=int)

stackidx=0
stacklen=np.zeros([20,1],dtype=int)
polystack=np.zeros([20,20,2],dtype=int)
def draw_poly(event,x,y,flags,param):
	global stackidx
	if event == cv2.EVENT_MOUSEMOVE:
		curpos[0]=x
		curpos[1]=y
	if event == cv2.EVENT_RBUTTONUP:
		polystack[stackidx,stacklen[stackidx],0]=x
		polystack[stackidx,stacklen[stackidx],1]=y
		stacklen[stackidx]+=1
	if event == cv2.EVENT_LBUTTONDBLCLK:
		polystack[stackidx,stacklen[stackidx],0]=x
		polystack[stackidx,stacklen[stackidx],1]=y
		stacklen[stackidx]+=1
		stackidx+=1
		curlen = np.array([stackidx])
		np.savez("obstacle",polystack,stacklen,curlen)
def labelStaticObstacle(M,warpscale):
	global stackidx
	global stacklen
	global polystack
	if os.path.isfile("obstacle.npz"):
		savedt=np.load("obstacle.npz")
		stackidx=savedt['arr_2'][0]
		polystack=savedt['arr_0']
		stacklen=savedt['arr_1']
	# img = cv2.imread("Frame/000020.jpg")
	# cv2.namedWindow('Obstacle',cv2.WINDOW_NORMAL)
	# cv2.setMouseCallback('Obstacle',draw_poly)
	# while(1):
	# 	drawImg = cv2.warpPerspective(img,M,(3*warpscale,3*warpscale))
	# 	for i in range(0,stackidx):
	# 		if stacklen[i]>0:
	# 			for j in range(1,int(stacklen[i])):
	# 				x_0=polystack[i,j-1,0]
	# 				y_0=polystack[i,j-1,1]
	# 				x_1=polystack[i,j,0]
	# 				y_1=polystack[i,j,1]
	# 				cv2.line(drawImg,(x_0,y_0),(x_1,y_1),(0,0,255),2)
	# 			cv2.line(drawImg,(polystack[i,stacklen[i]-1,0],polystack[i,stacklen[i]-1,1]),(polystack[i,0,0],polystack[i,0,1]),(0,0,255),2)
	# 	if (stacklen[stackidx])>0:
	# 		for i in range(1,int(stacklen[stackidx])):
	# 			cv2.line(drawImg,(polystack[stackidx,i-1,0],polystack[stackidx,i-1,1]),(polystack[stackidx,i,0],polystack[stackidx,i,1]),(255,0,0),2)
	# 		cv2.line(drawImg,(polystack[stackidx,int(stacklen[stackidx])-1,0],polystack[stackidx,int(stacklen[stackidx])-1,1]),(curpos[0],curpos[1]),(255,0,0),2)
	# 	cv2.putText(drawImg,"%d"%(stacklen[0]),(0,50),cv2.FONT_HERSHEY_PLAIN,1,(0,255,0),1)
	# 	cv2.imshow('Obstacle',drawImg)
	# 	c=cv2.waitKey(20)
	# 	if c==27:
	# 		cv2.destroyWindow("Obstacle")
	# 		break
	o=Obstacle()
	o.polystack=polystack
	o.stacklen=stacklen
	o.stackidx=stackidx
	return o