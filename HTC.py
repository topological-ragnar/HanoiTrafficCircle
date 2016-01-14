from numpy import matrix
from numpy import sin
from numpy import cos
from numpy.linalg import norm
from numpy import dot
from random import randrange
import matplotlib.pyplot as plt 


class car(object):
	"""represents a robocar"""
	def __init__(self, position, velocity, tolerance):
		"""position and velocity should be row matrices, tolerance is a length, and haste is a multiplier ~ 1+epsilon"""
		self.position = position
		self.velocity = velocity
		self.tolerance = tolerance


	def move(self,dt):
		self.position += self.velocity*dt

	def throttle(self,others,dt,accel):
		futureposition = self.position+self.velocity*dt
		slowed = False
		for othercar in others:
			otherfutureposition = othercar.position+othercar.velocity*dt
			#the car slows if it thinks it will collide with a faster car
			if (norm(otherfutureposition-futureposition)<self.tolerance) and norm(othercar.velocity)>norm(self.velocity):
				#it's got good brakes. it slows exponentially fast
				self.velocity/=2
				slowed = True
				break
		#otherwise it speeds up! (not exponentially though, that was ridiculous)
		if not slowed:
			self.velocity += accel*self.velocity*dt/norm(self.velocity)

def collisions(cars,col):
	dists = [c!=d and (norm(c.position-d.position),c.position) or (1,c.position) for c in cars for d in cars]
	dists = filter(lambda (x,c):x<col,dists)
	xcols = [a[1][0,0] for a in dists]
	ycols = [a[1][0,1] for a in dists]
	return [xcols,ycols]

def isvisibleto(d,c,vis):
	#this is not so important, so the visible space to a car is an infinite strip of width vis between the frontal plane (anatomy term) and the plane parallel to it a distance vis in front. one should probably cut
	return 0 < dot(d.position-c.position,c.velocity.T)/norm(c.velocity) < vis

def HTC(N,T=1,dt=0.01,vmax=1,tol=0.1,vis=0.5,accel=20,col=0.03):
	"""N=15 is a good number for this size simulation. set tol=0, col=0, N>>44^2 for an easter egg."""

	#initialize cars
	cars = []
	for j in range(N):
		theta = randrange(0,44)/7.
		start = matrix([sin(theta),cos(theta)])
		zeta = randrange(0,44)/7.
		destination = matrix([sin(zeta),cos(zeta)])
		V = vmax*(destination-start)
		cars.append(car(start,V,tol))

	#get initial positions
	xs = [c.position[0,0] for c in cars]
	ys = [c.position[0,1] for c in cars]

	#intialize plots
	fig, ax = plt.subplots()
	
	#plot initial positions
	points, = ax.plot(xs,ys,marker='o', linestyle ='None')
	ax.set_xlim(-1.5,1.5)
	ax.set_ylim(-1.5,1.5)
	
	#run the simulation
	for k in range(int(T/dt)):
		#each car adjusts its throttle and then moves
		for c in cars:
			visible = filter(lambda d:d!=c and isvisibleto(d,c,vis),cars)
			c.throttle(visible,dt,accel)
			c.move(dt)
		#get updated positions
		xs = [c.position[0,0] for c in cars]
		ys = [c.position[0,1] for c in cars]

		#plot any collisions
		cols = collisions(cars,col)
		ax.plot(cols[0],cols[1],marker='+',c='r', linestyle='None')		

		#update car positions in plot
		points.set_data(xs,ys)
		plt.pause(0.05)
		
		
