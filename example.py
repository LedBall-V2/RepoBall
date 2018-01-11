# ADXL345 Python example 

#import library
from adxl345 import ADXL345
import time 
import math
  
#create new object
adxl345 = ADXL345()

#set moving variable to false
moving = False


#algorithm to calculate velocity
#credits to: Tibo VandeMoortele
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

while True:
	
	def measure():

		#get values from axes
		axes = adxl345.getAxes(True)
		
		#place axes in variables
		x = float(axes['x'])
		y = float(axes['y'])
		z = float(axes['z'])
		print "---------------------------------"
		
		#save velocity in variable
		velc = calcVel(x, y, z)	
		
		#function: control if ball is moving
		def bigMovement():
			#function: see if ball is thrown
			print "ball is moving fast"
			moving = True
			time.sleep(5)
		def smallMovement():
			#function: see if ball is rolling
			print "ball is moving slowly"
			moving = False
			time.sleep(5)
		def noMovement():
			#function: see if ball is not moving
			print "ball is not moving"
			moving = False
		
		#function: ball hits an object
		def stopMovement():
			#check if  ball is moving
			if moving == True:
				#check if ball hit anything
				if velc > -1 and velc < 1:
					print "bal hit an object"
					moving = False
					time.sleep(5)
			else:
				#exit code or will give runtime errors
				exit()

		#if structure: control if ball is moving or not
		if velc > 6:
			bigMovement()
		
		elif velc > 3:
			smallMovement()
		else:
			noMovement()
		
		time.sleep(0.1)	

	measure()
	#stopMovement()
