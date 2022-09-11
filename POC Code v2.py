# -*- coding: utf-8 -*-
'''
Project 3 Robot Code
Brendan McLaughlin, Dan Powely, Ryan Williams, Gabe Wills
POC 1 Program

'''

import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers
import grovepi  # import the GrovePi drivers

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class

#Initiate the pins and modes of the sensors
line_finderL = 7
line_finderR = 2
ultrasonic_ranger = 6
hall_sensor = 1
grovepi.pinMode(line_finderL,"INPUT")
grovepi.pinMode(line_finderR,"INPUT")

speed = -30 #General speed of the MACRO when moving forward
sleepTime = 0.05 #Amount of time the robot rests before checking for the line again
sightDistance = 10 #cm to object at which the MACRO will stop
magnetThreshold = 20 #Maximum value that Hall Sensor can detect to pick up a magnet 
unload = False
onPath = False
direction = 'R'
upSpeed = 20 #Speed at which the forward motor turns when turning
backSpeed = -15 #Speed at which the backward motor turns when turning
lowerSpeed = 30 #Power used to lower the back gate of the MACRO when unloading

def trace(): #Prints out the results of the sensors to trace program for errors
    print("L: ", grovepi.digitalRead(line_finderL))
    print("R: ", grovepi.digitalRead(line_finderR))
    return

def setTurnVector(left, right):
    BP.set_motor_power(BP.PORT_A, right)
    BP.set_motor_power(BP.PORT_D, left)
    
    return

def turnLeft():
    print("Left Turn")
    while True:
        while (grovepi.digitalRead(line_finderL) == 1): 
            setTurnVector(backSpeed, upSpeed) #Set turning power of motors
            trace()
            if (grovepi.digitalRead(line_finderR) == 1 and grovepi.digitalRead(line_finderL) == 1):
                return
        BP.set_motor_power(BP.PORT_A+BP.PORT_D,speed)
        time.sleep(sleepTime)
        return
    
def turnRight():
    print("Turn Right")
    while True:
        while (grovepi.digitalRead(line_finderR) == 1): # While seeing line
            setTurnVector(upSpeed, backSpeed)
            trace()
            if (grovepi.digitalRead(line_finderR) == 1 and grovepi.digitalRead(line_finderL) == 1):
                return
        BP.set_motor_power(BP.PORT_A+BP.PORT_D, speed)
        time.sleep(sleepTime)
        return

def selectPath():
    BP.reset_all()
    BP.set_motor_power(BP.PORT_A+BP.PORT_D,speed + 10)
    time.sleep(0.125)
    BP.reset_all()
    time.sleep(1)
    print("Selecting Path")
    if (direction == 'R'):     
        print("Turn Across Left Line")
        while(grovepi.digitalRead(line_finderL) == 1): #Turns across the opposing track when both sensors are tripped
            BP.set_motor_power(BP.PORT_A, 20)
            BP.set_motor_power(BP.PORT_D, -20)
            trace()
        turnRight()
    else:
        print("Turn Across Right Line")
        while(grovepi.digitalRead(line_finderR) == 1):
            BP.set_motor_power(BP.PORT_A, -20)
            BP.set_motor_power(BP.PORT_D, 20)
            trace()
        turnLeft()
    
    print("Across The Line")
    while not(grovepi.digitalRead(line_finderR) == 1 and grovepi.digitalRead(line_finderL) == 1):
        print("Following Selected Path")
        BP.set_motor_power(BP.PORT_A+BP.PORT_D, speed)
        time.sleep(0.2)
        trace()
        if (grovepi.ultrasonicRead(ultrasonic_ranger) < sightDistance): #Stop if seeing something
            BP.reset_all()
        if (grovepi.digitalRead(line_finderL) == 1): #Turn left
            turnLeft()
            time.sleep(sleepTime)
        elif (grovepi.digitalRead(line_finderR) == 1): #Turn right
            turnRight()
            time.sleep(sleepTime)
    print("Hit Second Path")
    BP.set_motor_power(BP.PORT_A+BP.PORT_D,speed + 10)
    time.sleep(1.5)
    return
    
def unloadCargo():
    BP.set_motor_power(BP.PORT_A+BP.PORT_D, speed)
    time.sleep(1) #Go in front so the cargo slides into place
    
    BP.set_motor_power(BP.PORT_B, lowerSpeed) #Raise and lower the cargo gate
    time.sleep(3)
    BP.set_motor_power(BP.PORT_B, 0)
    time.sleep(2)
    BP.set_motor_power(BP.PORT_B, lowerSpeed * -1)
    time.sleep(3)
    BP.reset_all()

    return

try:
    while True:
        BP.set_motor_power(BP.PORT_A+BP.PORT_D, speed)
        trace()
        if (grovepi.ultrasonicRead(ultrasonic_ranger) < sightDistance): #Stop if seeing something
            BP.reset_all()
        if (grovepi.digitalRead(line_finderL) == 1): #Turn left
            turnLeft()
            time.sleep(sleepTime)
        elif (grovepi.digitalRead(line_finderR) == 1): #Turn right
            turnRight()
            time.sleep(sleepTime)
        if (grovepi.digitalRead(line_finderL) == 1 and grovepi.digitalRead(line_finderR) == 1): #select path 
            BP.reset_all()
            selectPath()
            #unload = True
        elif(grovepi.digitalRead(hall_sensor) < 20 and unload): #Unload cargo
            BP.reset_all()
            unloadCargo()
    
except KeyboardInterrupt:
    BP.reset_all()
