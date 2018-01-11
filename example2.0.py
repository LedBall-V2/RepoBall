# ADXL345 Python example 

#import library
from adxl345 import ADXL345
import time 
import math
  
#create new object
adxl345 = ADXL345()

#create variable to check for movement
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
	
	#this is the basic function which will be continously executed
	def measure():

		#get values from axes
		axes = adxl345.getAxes(True)
		
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

                        #set timer for now + a couple of seconds
                        t = time.time() + 1

                        #while lus till time has ran out
                        while time.time() < t:

                                #check if  ball is moving
                                if moving == True:
					
					#ask values of axes
					axes = adxl345.getAxes(True)
					x = float(axes['x'])
					y = float(axes['y'])
					z = float(axes['z'])
					print(x)
					print(y)
					print(z)
				
					#recalculate values
					velc = calcVel(x, y, z)
					                                        
					#check if ball hit anything
                                        if velc > -0.1 and velc < 0.1:
                                                print "bal hit an object"
                                                moving = False
                                                time.sleep(5)
                                
				else:
                                        #exit code or will give runtime errors
                                        #don't forget to reset hit
                                        moving = False
					print "ball didn't hit anything"
					time.sleep(5)
                                        exit()
		

		#functions: to detect movements
                def bigMovement():
			#in every function you need to call the global variable
			global moving

                        #function: see if ball is thrown
                        moving = True
                        
                        #call stopmovement function
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
		if velc > 12 :
			bigMovement()
		
		elif velc > 3:
			smallMovement()
		else:
			noMovement()
			

	#permanently check values
	measure()
