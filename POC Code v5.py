# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 00:58:43 2021

@author: btmcl

Project 3 Robot Code
Brendan McLaughlin, Dan Powely, Ryan Williams, Gabe Wills
POC Program version 4

"""

import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers
import grovepi  # import the GrovePi drivers
from MPU9250 import MPU9250 #import the IMU drivers

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class

mpu9250 = MPU9250() # Initialize the MPU9250 library

#Initiate the pins and modes of the sensors
line_finderL = 2
line_finderR = 7
ultrasonic_ranger = 6
grovepi.pinMode(line_finderL,"INPUT")
grovepi.pinMode(line_finderR,"INPUT")

#General Variable Initiation
speed = -30             #General speed of the MACRO when moving forward
sleepTime = 0.05        #Amount of time the robot rests before checking for the line again
sightDistance = 10      #cm to object at which the MACRO will stop
upSpeed = -30           #Speed at which the forward motor turns when turning
backSpeed = 25          #Speed at which the backward motor turns when turning
lowerSpeed = -30        #Power used to lower the back gate of the MACRO when unloading
junctionCount = 0       #Number of junctions crossed when navigating the track
beaconCount = 0         #Number of magnetic beacons that have been detected
gyroThreshold = 12       #Value of gyroscope at which to increase the power at a hill
turboSpeed = 2.5        #Factor to increase power by when driving over hill
turbo = True            #Whether to activate the turbo or not
stillTurbo = False       #Used to keep turbo from activating and deactivating repeatedly
stillSeeingMag = False  #Used to keep from seeing the magnet more than one time
turboCount = 0

#Directions for MACRO to follow around the given course
lapDirections = ['L','L','L','R','L','R','R',     #Lap 1 Turns
                 'L','L','L','L','R','L','R',     #Lap 2 Turns
                 'L','L','L','L','L','L']         #Lap 3 Turns
unloadAtBeacon = [False, True, False, False, False, True, 
                  False, False, False, True, False]         #Whether to unload at a specific beacon

def trace(): #Prints out the results of the sensors to trace program for errors
    print("L: ", grovepi.digitalRead(line_finderL))
    print("R: ", grovepi.digitalRead(line_finderR))
    print("")
    return

def setTurnVector(left, right): #Sets the power in each motor for turning
    BP.set_motor_power(BP.PORT_D, left)
    BP.set_motor_power(BP.PORT_A, right)
    return

def turnLeft(mag):
    print("Left Turn")
    while (grovepi.digitalRead(line_finderL) == 1): 
        setTurnVector(backSpeed, upSpeed) #Set turning power of motors
        trace()
        if (grovepi.digitalRead(line_finderR) == 1 and grovepi.digitalRead(line_finderL) == 1):
            print("Break out of Left Turn")
            return #Breaks out in case of junction detection
        if not(mag['x']):
            print("Break Out to Count Magnet")
            return #Breaks out in case of magnetic beacon detection
        time.sleep(sleepTime)
    return
    
def turnRight(mag):
    print("Right Turn")
    while (grovepi.digitalRead(line_finderR) == 1): # While seeing line
        setTurnVector(upSpeed, backSpeed)
        trace()
        if (grovepi.digitalRead(line_finderR) == 1 and grovepi.digitalRead(line_finderL) == 1):
            print("Break out of Right Turn")
            return #Breaks out in case of junction detection
        if not(mag['x']):
            print("Break Out to Unload")
            return #Breaks out in case of magnetic beacon detection
        time.sleep(sleepTime)
    return

def selectPath(junctionCount):
    BP.reset_all()
    BP.set_motor_power(BP.PORT_A+BP.PORT_D, -10)    #Crosses a very thin line in the case of the hill border
    time.sleep(0.25)
    BP.reset_all()
    if not(grovepi.digitalRead(line_finderL) == 1 and grovepi.digitalRead(line_finderR) == 1):
        print("Crossing Hill Border Line")
        return
    print("Selecting Path")
    
    if (lapDirections[junctionCount] == 'R'):  #Get directions from the directions array for given junction
        print("Selecting Right Path\n")
        print("Turning Across Left Line")
        while (grovepi.digitalRead(line_finderL) == 1):  #Turn until the left sensor is completely acrsoss the line
            setTurnVector(upSpeed * -1.5, backSpeed * -1)
            trace()
            time.sleep(sleepTime)
            
        print("Moving Until Left Sensor Sees Line")
        while (grovepi.digitalRead(line_finderL) != 1):  #Drive forward until the line is hit again
            BP.set_motor_power(BP.PORT_A+BP.PORT_D, speed)
            trace()
            time.sleep(sleepTime)
    else:
        print("Selecting Left Path\n")
        print("Turning Across Right Line")
        while (grovepi.digitalRead(line_finderR) == 1):  #Turn until the right sensor is completely across the line
            setTurnVector(backSpeed * -1, upSpeed * -1.5)
            trace()
            time.sleep(sleepTime)
        
        print("Moving Until Right Sensor Sees Line")    
        while (grovepi.digitalRead(line_finderR) != 1):  #Drive forward until the line is hit again
            BP.set_motor_power(BP.PORT_A+BP.PORT_D, speed)
            trace()
            time.sleep(sleepTime)
            
        print("\n\n----Function Close----\n\n")
    
    return
    
def unloadCargo():
    print("Unloading Cargo")
    BP.reset_all()
    time.sleep(1)
    BP.set_motor_power(BP.PORT_A+BP.PORT_D, speed)
    time.sleep(2.75) #Go in front so the cargo slides into place
    BP.reset_all()
    
    BP.set_motor_power(BP.PORT_B, lowerSpeed) #Raise and lower the cargo gate
    time.sleep(3)
    BP.set_motor_power(BP.PORT_B, 0)
    time.sleep(2)
    BP.set_motor_power(BP.PORT_A+BP.PORT_D, speed)
    time.sleep(0.75)
    BP.reset_all()
    BP.set_motor_power(BP.PORT_B, lowerSpeed * -1)
    time.sleep(2.25)
    
    BP.set_motor_power(BP.PORT_A+BP.PORT_D, speed * -1)
    time.sleep(1.25) #Move backwards to return to drop off spot
    BP.reset_all()

    return

'''
def sportMode(): #ACITVATE TURBOCHARGER
    print("Powering Over Hill")
    BP.set_motor_power(BP.PORT_A+BP.PORT_D, speed * turboSpeed)
    time.sleep(1.4)
    return
'''

try:
    while True:
        BP.set_motor_power(BP.PORT_A+BP.PORT_D, speed)
        gyro = mpu9250.readGyro()
        mag = mpu9250.readMagnet()
        print("Gyro X: ", gyro['x'])
        #print('Magnet Z: ', mag['x'])
        #print("Junction Count: ", junctionCount)
        #print("Beacon Count: ", beaconCount)
        #trace()
        if not(mag['x']): #Check to unload if seeing a magnetic beacon
            if (unloadAtBeacon[beaconCount] and not stillSeeingMag):
                unloadCargo()
            if not(stillSeeingMag):
                beaconCount += 1
            stillSeeingMag = True
            turbo = True
        else:
            stillSeeingMag = False
        if (gyro['x'] > gyroThreshold): #Boost over the hill when it is detected
            if (turbo and not stillTurbo):
                print("Entering Turbo Mode")
                speed *= 2.5
                turbo = False
                stillTurbo = True
                turboCount += 1
                print("Turbo Count: ", turboCount)
            elif not(stillTurbo) and not turbo and turboCount == 3:
                print("Exiting Turbo Mode")
                speed /= 2.5
                turbo = True
                stillTurbo = True
                turboCount = 0
            elif not(stillTurbo) and not turbo:
                turboCount += 1
                print("Turbo Count: ", turboCount)
            
        else:
            stillTurbo = False
        if (grovepi.ultrasonicRead(ultrasonic_ranger) < sightDistance): #Stop if seeing something within range
            print("Too Close")
            while (grovepi.ultrasonicRead(ultrasonic_ranger) < sightDistance):  #Stay stopped until obstacle moves
                BP.reset_all()
        elif (grovepi.digitalRead(line_finderL) == 1): #Turn left
            turnLeft(mag)
        elif (grovepi.digitalRead(line_finderR) == 1): #Turn right
            turnRight(mag)
        if (grovepi.digitalRead(line_finderL) == 1 and grovepi.digitalRead(line_finderR) == 1): #Select path
            selectPath(junctionCount)
            junctionCount += 1
        time.sleep(sleepTime)
    
except KeyboardInterrupt:
    BP.reset_all()
