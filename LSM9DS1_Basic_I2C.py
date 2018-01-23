#!/usr/bin/env python
# coding: utf-8

#import ctypes
from ctypes import *
import time
import math
import sys
import urllib2

#create variable to check for movement
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
	print v2
	return v2

path = "../lib/liblsm9ds1cwrapper.so"
lib = cdll.LoadLibrary(path)

lib.lsm9ds1_create.argtypes = []
lib.lsm9ds1_create.restype = c_void_p

lib.lsm9ds1_begin.argtypes = [c_void_p]
lib.lsm9ds1_begin.restype = None

lib.lsm9ds1_calibrate.argtypes = [c_void_p]
lib.lsm9ds1_calibrate.restype = None

lib.lsm9ds1_gyroAvailable.argtypes = [c_void_p]
lib.lsm9ds1_gyroAvailable.restype = c_int
lib.lsm9ds1_accelAvailable.argtypes = [c_void_p]
lib.lsm9ds1_accelAvailable.restype = c_int
lib.lsm9ds1_magAvailable.argtypes = [c_void_p]
lib.lsm9ds1_magAvailable.restype = c_int

lib.lsm9ds1_readGyro.argtypes = [c_void_p]
lib.lsm9ds1_readGyro.restype = c_int
lib.lsm9ds1_readAccel.argtypes = [c_void_p]
lib.lsm9ds1_readAccel.restype = c_int
lib.lsm9ds1_readMag.argtypes = [c_void_p]
lib.lsm9ds1_readMag.restype = c_int

lib.lsm9ds1_getGyroX.argtypes = [c_void_p]
lib.lsm9ds1_getGyroX.restype = c_float
lib.lsm9ds1_getGyroY.argtypes = [c_void_p]
lib.lsm9ds1_getGyroY.restype = c_float
lib.lsm9ds1_getGyroZ.argtypes = [c_void_p]
lib.lsm9ds1_getGyroZ.restype = c_float

lib.lsm9ds1_getAccelX.argtypes = [c_void_p]
lib.lsm9ds1_getAccelX.restype = c_float
lib.lsm9ds1_getAccelY.argtypes = [c_void_p]
lib.lsm9ds1_getAccelY.restype = c_float
lib.lsm9ds1_getAccelZ.argtypes = [c_void_p]
lib.lsm9ds1_getAccelZ.restype = c_float

lib.lsm9ds1_getMagX.argtypes = [c_void_p]
lib.lsm9ds1_getMagX.restype = c_float
lib.lsm9ds1_getMagY.argtypes = [c_void_p]
lib.lsm9ds1_getMagY.restype = c_float
lib.lsm9ds1_getMagZ.argtypes = [c_void_p]
lib.lsm9ds1_getMagZ.restype = c_float

lib.lsm9ds1_calcGyro.argtypes = [c_void_p, c_float]
lib.lsm9ds1_calcGyro.restype = c_float
lib.lsm9ds1_calcAccel.argtypes = [c_void_p, c_float]
lib.lsm9ds1_calcAccel.restype = c_float
lib.lsm9ds1_calcMag.argtypes = [c_void_p, c_float]
lib.lsm9ds1_calcMag.restype = c_float

#creat object and check if it's available
if __name__ == "__main__":
    imu = lib.lsm9ds1_create()
    lib.lsm9ds1_begin(imu)
    if lib.lsm9ds1_begin(imu) == 0:
        print("Failed to communicate with LSM9DS1.")
        quit()
    lib.lsm9ds1_calibrate(imu)

    #loop
    while True:
	try:
		#check if gyro is online
        	while lib.lsm9ds1_gyroAvailable(imu) == 0:
            		pass
        	lib.lsm9ds1_readGyro(imu)

		#check if accellero is online
		while lib.lsm9ds1_accelAvailable(imu) == 0:
            		pass
        	lib.lsm9ds1_readAccel(imu)
		

		def getValuesAcc():
			ax = lib.lsm9ds1_getAccelX(imu)
                        ay = lib.lsm9ds1_getAccelY(imu)
                        az = lib.lsm9ds1_getAccelZ(imu)

			cax = lib.lsm9ds1_calcAccel(imu, ax)
                        cay = lib.lsm9ds1_calcAccel(imu, ay)
                        caz = lib.lsm9ds1_calcAccel(imu, az)

			#return values
			return cax, cay, caz

		def getValuesGyro():
        		gx = lib.lsm9ds1_getGyroX(imu)
        		gy = lib.lsm9ds1_getGyroY(imu)
        		gz = lib.lsm9ds1_getGyroZ(imu)

        		cgx = lib.lsm9ds1_calcGyro(imu, gx)
        		cgy = lib.lsm9ds1_calcGyro(imu, gy)
        		cgz = lib.lsm9ds1_calcGyro(imu, gz)
			
			#return values
			return cgx, cgy, cgz

		#functions: to detect movement
		def bigMovement():
			#call global variable
			global moving

			#function: see if ball is thrown
			moving = True

			#call stop movement function
			#stopMovement()

		def smallMovement():
			global moving
			moving = False

		def noMovement():
			global moving
			moving = False

		#catch values
		cax, cay, caz = getValuesAcc()
		cgx, cgy, cgz = getValuesGyro()

        	print("Gyro: %f, %f, %f" % (cgx, cgy, cgz))
        	print("Accel: %f, %f, %f" % (cax, cay, caz))
		velc = calcVel(cax, cay, caz)
        	print "-------------------------"
		time.sleep(0.1)


		#if structure: control i ball is moving or not
		if velc > 5:
			bigMovement()
		elif velc > 3:
			smallMovement()
		else:
			noMovement



	#control + C -> shutdown application
	except KeyboardInterrupt:
		quit()
