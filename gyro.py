
#import library's
import time
import math
import IMU
import datetime
import os
import sys

RAD_TO_DEG = 57.29578
M_PI = 3.14159265358979323846
G_GAIN = 0.070
AA =  0.40

#variable to check moving
moving = False

gyroXangle = 0.0
gyroYangle = 0.0
gyroZangle = 0.0
CFangleX = 0.0
CFangleY = 0.0

IMU.detectIMU()     #Detect IMU
IMU.initIMU()       #Initialise the accelerometer, gyroscope and compass

#algorithm to calculate velocity
def calcVel(valueX, valueY, valueZ):
	xComb = valueX * valueX
	yComb = valueY * valueY
	zComb = valueZ * valueZ
	xyComb = xComb + yComb
	v1 = math.sqrt(xyComb)
	zv1Comb = zComb + v1
	v2 = math.sqrt(zv1Comb)
	print v2
	return v2

#loop
while True:

	#try: catch exceptions
	try:


		#Read the accelerometer values
    		def readAcc():
			ACCx = IMU.readACCx()
    			ACCy = IMU.readACCy()
    			ACCz = IMU.readACCz()
			x = ACCx * 0.000833333
                	y = ACCy * 0.000833333
                	z = ACCz * 0.000833333
			return x, y, z

		#Read the gyroscope values
		def readGyr():
    			GYRx = IMU.readGYRx()
    			GYRy = IMU.readGYRy()
    			GYRz = IMU.readGYRz()
			return GYRx, GYRy, GYRz

		#save accellero values in variables
		x, y, z = readAcc()
    		velc = calcVel(x, y, z)
    		print "-----------------------------"


    		#Convert Gyro raw to degrees per second
    		rate_gyr_x =  GYRx * G_GAIN
    		rate_gyr_y =  GYRy * G_GAIN
    		rate_gyr_z =  GYRz * G_GAIN

		#function: ball hits an object
		def stopMovement():
			global moving

			#set timer
			t = time.time() + 1

			#while lus: till time runs out
			while time.time() < t:

				#check if ball is moving
				if moving == True:
					#re-ask values of accellero
					x, y, z = readAcc()

					#re-calculate velocity
					velc = calcVel(x, y, z)

					#check if ball hit anything
					if velc < 0.5:
						#ball hit an object
						print "ball hit an object"
						moving = False

						#start timer
						t = time.time() + 1

						#while lus: check if person catched the ball
						while time.time() < t:

							#recalculate values
							x, y, z = readAcc()

							#recalculate velocity
							velc = calcVel(x, y, z)

							#if structure: check if person catched the ball
							if velc > 3:
								print "HIT"
								time.sleep(3)

							else:
								"Person catched the ball"
								time.sleep(3)

				else:
					#exit code or will give runtime errors
					#don't forget to reset hit
					moving = False
					print "ball didn't hit anything"
					exit()

		#functions: to check movement
		def bigMovement():
			#in every function you need to call the global varialbe
			global moving

			#function: see if ball is thrown
			moving = True

			#call stop movement function
			stopMovement() 

		def smallMovement():
			global moving
			moving = False

		def noMovement():
			global moving
			moving = False

		#if structure: control if ball is moving or not
		if velc > 8:
			bigMovement()
		elif velc > 3:
			smallMovement()
		else:
			noMovement()





	#exceptions
	#ctrl + c interrupt
	except KeyboardInterrupt:
		#shut down code
		exit()
