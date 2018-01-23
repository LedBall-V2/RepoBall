#ADXL345 Python

#import library's
from adxl345 import ADXL345
import time
import math
import urllib2
import sys
import bluetooth

#set settings for bluetooth
serverMACAddress = 'b8:27:eb:21:94:86'
port = 3
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.connect((serverMACAddress, port))

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

	#global variable aanroepen
	global s

	try:
		s.send(str(v2))
		time.sleep(0.001)
	except bluetooth.btcommon.BluetoothError as error:
		print "connection bluetooth lost"
		s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
		s.connect((serverMACAddress, port))
	return v2

#loop
while True:

	try:

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
						if velc < 0.5:
							print "ball hit an object"
							s.send("hit")
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
								if velc > 4:
									print "ball falls to ground"
									time.sleep(1)
									s.send("Ball falls")

								else:
									print "Person catched the ball"
									s.send("Ball catch")
									time.sleep(3)


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
		# check if internet is on
		#def internet_on():
		#	try:
		#		urllib2.urlopen('http://192.168.1.1', timeout=3)
		#		return True
		#	except urllib2.URLError as err:
		#		return False


		#if internet_on() == True:
		#	measure()
		#else:
		#	sys.exit("No internet connection")

		measure()
	
	#bij control + c programma afsluiten
	except KeyboardInterrupt:
		sock.close()
