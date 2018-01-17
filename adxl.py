#ADXL345 Python

#import library's
from adxl345 import ADXL345
import time
import math

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
	print(v2)
	return v2

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
					if velc < 0.1:
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
								time.sleep(10)

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
		if velc > 8:
			bigMovement()
		elif velc > 3:
			smallMovement()
		else:
			noMovement()


	#permanently check values
	measure(
        time.sleep(0.01)
