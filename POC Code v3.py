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

#General Variable Initiation
speed = -30             #General speed of the MACRO when moving forward
sleepTime = 0.05        #Amount of time the robot rests before checking for the line again
sightDistance = 10      #cm to object at which the MACRO will stop
magnetThreshold = 20    #Maximum value that Hall Sensor can detect to pick up a magnet 
unload = False           #Only changes if magnets are required to detect junctions
direction = 'L'         #Direction to turn at detected junction
upSpeed = 20            #Speed at which the forward motor turns when turning
backSpeed = -15         #Speed at which the backward motor turns when turning
lowerSpeed = 30         #Power used to lower the back gate of the MACRO when unloading

def trace(): #Prints out the results of the sensors to trace program for errors
    print("L: ", grovepi.digitalRead(line_finderL))
    print("R: ", grovepi.digitalRead(line_finderR))
    print("Hall Sensor: ", grovepi.digitalRead(hall_sensor))
    return

def setTurnVector(left, right): #Sets the power in each motor for turning
    BP.set_motor_power(BP.PORT_D, left)
    BP.set_motor_power(BP.PORT_A, right)
    return

def turnLeft():
    print("Left Turn")
    while (grovepi.digitalRead(line_finderL) == 1): 
        setTurnVector(backSpeed, upSpeed) #Set turning power of motors
        trace()
        if (grovepi.digitalRead(line_finderR) == 1 and grovepi.digitalRead(line_finderL) == 1):
            print("Break out of Left Turn")
            return #Breaks out in case of junction detection
    return
    
def turnRight():
    print("Right Turn")
    while (grovepi.digitalRead(line_finderR) == 1): # While seeing line
        setTurnVector(upSpeed, backSpeed)
        trace()
        if (grovepi.digitalRead(line_finderR) == 1 and grovepi.digitalRead(line_finderL) == 1):
            print("Break out of Right Turn")
            return #Breaks out in case of junction detection
    return

def selectPath():
    BP.reset_all()
    BP.set_motor_power(BP.PORT_A+BP.PORT_D, -10)
    time.sleep(0.25)
    BP.reset_all()
    if not(grovepi.digitalRead(line_finderL) == 1 and grovepi.digitalRead(line_finderR) == 1):
        print("Crossing Hill Border Line")
        return
    print("Selecting Path")
    
    if (direction == 'R'):
        print("Selecting Right Path")
        trace()
        print("Turning Across Left Line")
        while (grovepi.digitalRead(line_finderL) == 1):
            setTurnVector(upSpeed * -1.5, backSpeed * -1)
            trace()
            
        print("Turning Until Left Sensor Is Off Line")
        while (grovepi.digitalRead(line_finderL) != 1):
            BP.set_motor_power(BP.PORT_A+BP.PORT_D, speed)
            trace()
    else:
        print("Selecting Left Path")
        trace()
        print("Turning Across Right Line")
        while (grovepi.digitalRead(line_finderR) == 1):
            setTurnVector(backSpeed * -1, upSpeed * -1.5)
            trace()
            
        print("Turning Until Right Sensor Is Off Line")
        while (grovepi.digitalRead(line_finderR) != 1):
            BP.set_motor_power(BP.PORT_A+BP.PORT_D, speed)
            trace()
            
        print("\n\n---Function Close---\n\n")
    
    return
    
def unloadCargo():
    print("Unloading Cargo")
    BP.reset_all()
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

def powerOver(): #Moves back and then powers forward with high speed to clear hills
    BP.reset_all()
    BP.set_motor_power(BP.PORT_A+BP.PORT_D, -1 * speed)
    time.sleep(0.4)
    BP.set_motor_power(BP.PORT_A+BP.PORT_D, speed * 1.5)
    time.sleep(1.3)
    BP.set_motor_power(BP.PORT_A+BP.PORT_D, speed)
    return

try:
    while True:
        BP.set_motor_power(BP.PORT_A+BP.PORT_D, speed)
        trace()
        if (grovepi.ultrasonicRead(ultrasonic_ranger) < sightDistance): #Stop if seeing something within range
            print("Too Close")
            while (grovepi.ultrasonicRead(ultrasonic_ranger) < sightDistance):
                BP.reset_all()
        elif (grovepi.digitalRead(line_finderL) == 1): #Turn left
            turnLeft()
        elif (grovepi.digitalRead(line_finderR) == 1): #Turn right
            turnRight()
        if (grovepi.digitalRead(line_finderL) == 1 and grovepi.digitalRead(line_finderR) == 1): #Select path 
            selectPath()
        elif((not grovepi.digitalRead(hall_sensor)) and unload): #Unload cargo
            unloadCargo()
        time.sleep(sleepTime)
    
except KeyboardInterrupt:
    BP.reset_all()
