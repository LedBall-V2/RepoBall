#ADXL345 Python

#import library's
from adxl345 import ADXL345
import time
import math
import urllib2
import sys

#create new object
adxl = ADXL345()

#Create variable to check for movement
moving = False


#algorithm to calculate velocity
def calcVel(valueX, valueY, valueZ):
	xComb = valueX * valueX
	yComb = valueY * valueY
	zComb = valueZ * valueZ
	xyComb = xComb + yComb
	v1 = math.sqrt(xyComb)
	zv1Comb = zComb + v1
	v2 = math.sqrt(zv1Comb)
	#print(v2)
	return v2

#algorithm to calculate degrees of ball
def checkDegrees():
    #get values from axes
    axes = adxl.getAxes(True)

    #place axes in variables
    x = float(axes['x'])
    y = float(axes['y'])
    z = float(axes['z'])

    #check if values are zero (ZeroDivideError)
    if x == 0.000:
       x = 0.001
    if y == 0.000:
       y = 0.001
    if z == 0.000:
       z = 0.001

    #calculate corner ball
    #radials
    c1 = math.atan2(y, x)
    c2 = math.atan2(z, y)

    #set radials to degree
    c1 = c1 / (2 * math.pi) * 360
    c2 = c2 / (2 * math.pi) * 360
    time.sleep(2)

    return c1, c2

#loop
while True:

	#function: which will be called continously
	def measure():

		#get values from axes
		axes = adxl.getAxes(True)

		#place axes in variables
		x = float(axes['x'])
		y = float(axes['y'])
		z = float(axes['z'])

		#save velocity in variable
		velc = calcVel(x, y, z)

        #call function to check degrees of ball
        c1, c2 = checkDegrees()
        print("Degrees corner 1: %.3FG" % c1)
        print("Degrees corner 2: %.3FG" % c2)

		#function: ball hits an object
		def stopMovement():
			#in every function you need to call the global variable
			global moving

			#set time for now + a couple of seconds
			t = time.time() + 1

			#while lus: till time runs out
			while time.time() < t:

				#check if ball is moving
				if  moving == True:

					#ask values of axes
					axes = adxl.getAxes(True)
					x = float(axes['x'])
					y = float(axes['y'])
					z = float(axes['z'])

					#recaculate velocity
					velc = calcVel(x, y, z)

					#check if ball hit anything
					if velc < 0.3:
						print "ball hit an object"
						moving = False
						
						#start time
						t = time.time() + 1

						#while lus: check if person catched the ball
						while time.time() < t:

							#recalculate values
							axes = adxl.getAxes(True)
							x = float(axes['x'])
							y = float(axes['y'])
							z = float(axes['z'])

							#recalculate velocity
							velc = calcVel(x, y, z)

							#if structure : check if person catched the ball
							if velc < 1.5:
								print "person catched the ball"
								time.sleep(1)

							else:
								print "hit or miss"
								time.sleep(10)


				else:
					#exit code or will give runtime errors
					#don't forget to reset hit
					moving = False
					print "ball didn't hit anything"
					exit()


		#functions: to detect movements
		def bigMovement():
			#in every function you need to call the global variable
			global moving

			#function: see if ball is thrown
			moving = True

			#call stop movement function
			stopMovement()
		def smallMovement():
			#in every function you need to call the global variable
			global moving

			#function: see if ball is rolling
			moving = False
		def noMovement():
			#in every function you need to call the global variable
			global moving

			#function: see if ball is not moving
			moving = False


		#if structure: control if ball is moving or not
		if velc > 6:
			bigMovement()
		elif velc > 3:
			smallMovement()
		else:
			noMovement()


	# check if internet is on
	def internet_on():
		try:
			#ping to router
			urllib2.urlopen('http://192.168.1.1', timeout=3)
			return True
		except urllib2.URLError as err:
			return False

	if internet_on() == True:
		#function: check values
		measure()
	else:
		print "Internet connection lost"
		sys.exit("No internet connection")
