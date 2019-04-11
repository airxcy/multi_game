import math

def clamp(minv,maxv,v):
	v = min(v)
	return v
def angleLR(x0,y0,x1,y1,dirvec):
	## angle of 2 vectors and left/right sizes
	viewvec=[x1-x0,y1-y0]
	veclen = math.sqrt(viewvec[0]*viewvec[0]+viewvec[1]*viewvec[1])
	if veclen==0:
		return (0,0,0)
	viewvec[0]=viewvec[0]/veclen
	viewvec[1]=viewvec[1]/veclen
	dircos = viewvec[0]*dirvec[0]+viewvec[1]*dirvec[1]
	dircross = viewvec[0]*dirvec[1]-viewvec[1]*dirvec[0]
	lr_sides = 1-int(dircross>0)*2 ## -1 left?
	dircos=(dircos>1.0)*1.0+(dircos<=1.0)*dircos
	dircos=(dircos<-1.0)*(-1.0)+(dircos>=-1.0)*dircos
	rad = math.acos(dircos)
	return (lr_sides,rad,veclen)

def vec2Angle(x1,y1,x2,y2):
	dircos = x1*x2+y1*y2
	dircross = x1*y2-y1*x2
	lr_sides = 1-int(dircross>0)*2
	dircos=(dircos>1.0)*1.0+(dircos<=1.0)*dircos
	dircos=(dircos<-1.0)*(-1.0)+(dircos>=-1.0)*dircos
	rad = math.acos(dircos)
	return (lr_sides,rad)

def angleVec(dx,dy,rad):
	## angle of 2 vectors and left/right sizes
	vx=dx*math.cos(rad)-dy*math.sin(rad)
	vy=dx*math.sin(rad)+dy*math.cos(rad)
	return (vx,vy)


def projection2D(x,y,x1,y1):
	### x1*x1+y1*y2=1 Project x,y on to x1,y1 base coordinate system
	x2=x1*x+y1*y
	y2=x1*y-y1*x
	return (x2,y2)

def ReverseProjection2D(x2,y2,x1,y1):
	### x1*x1+y1*y2=1
	x=x1*x2-y1*y2
	y=y1*x2+x1*y2
	return (x,y)