from numpy import matrix
from numpy import sin
from numpy import cos
from random import randrange
import matplotlib.pyplot as plt 


class car(object):
	"""represents a robocar"""
	def __init__(self, position, velocity, tolerance, haste):
		"""position and velocity should be row matrices, tolerance is a length, and haste is a multiplier ~ 1+epsilon"""
		self.position = position
		self.velocity = velocity
		self.tolerance = tolerance
		self.haste = haste

	def move(self,dt):
		self.position += self.velocity*dt

	def throttle(self,others):
		futureposition = self.position+self.velocity*dt
		slowed = False
		for othercar in others:
			otherfutureposition = othercar.position+othercar.velocity*dt
			if abs(otherfutureposition-futureposition)<self.tolerance:
				self.velocity = self.velocity/2
				slowed = True
				break
		if not slowed:
			self.velocity *= self.haste

def HanoiTrafficCircle(N,T,dt,vmax,tol,haste):
	"""set tol=0 N>>44^2 for an easter egg"""
	cars = []
	for j in range(N):
		theta = randrange(0,44)/7.
		start = matrix([sin(theta),cos(theta)])
		zeta = randrange(0,44)/7.
		destination = matrix([sin(zeta),cos(zeta)])
		V = vmax*(destination-start)
		cars.append(car(start,V,tol,haste))

	xs = [c.position[0,0] for c in cars]
	ys = [c.position[0,1] for c in cars]

	fig, ax = plt.subplots()

	points, = ax.plot(xs,ys,marker='o', linestyle ='None')
	ax.set_xlim(-1.5,1.5)
	ax.set_ylim(-1.5,1.5)
	

	for k in range(T/dt):
		for c in cars:
			c.move(dt)
		xs = [c.position[0,0] for c in cars]
		ys = [c.position[0,1] for c in cars]
		points.set_data(xs,ys)
		plt.pause(0.05)
		
		
