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

# Connect the Grove Line Finder to digital port D7
# SIG,NC,VCC,GND
line_finder = 7
ultrasonic_ranger = 4
hall_sensor = 2
#grovepi.pinMode(line_finder,"INPUT")
BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.NXT_LIGHT_ON)

BP.offset_motor_encoder(BP.PORT_A, BP.get_motor_encoder(BP.PORT_A))
#BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B))
#BP.offset_motor_encoder(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C))
BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D))

def getColor():
    if(BP.get_sensor(BP.PORT_1)) < 2000:
        return 0
    return 1

def navigateToLine():
    BP.reset_all()
    
    while True:
        angle = 10
        while (getColor() == 0): # While not seeing line
            positionLeft = BP.get_motor_encoder(BP.PORT_A)
            positionRight = BP.get_motor_encoder(BP.PORT_D)
        
            BP.set_motor_position(BP.PORT_A, positionLeft + angle)
            BP.set_motor_position(BP.PORT_D, positionRight + angle*-1)\
            
            # Add 10 degrees to angle and reverses direction
            angle = (abs(angle) + 10) * angle / abs(angle) * -1
            print(angle)
            print(grovepi.digitalRead(line_finder))
            time.sleep(1)
        break
    return
    
def unloadCargo():
    return

try:
    while True:
        BP.set_motor_power(BP.PORT_A+BP.PORT_D,30)
        print(grovepi.digitalRead(line_finder))
        if (getColor() != 1):
            navigateToLine()
        if (grovepi.ultrasonicRead(ultrasonic_ranger)):
            BP.reset_all()
        if (grovepi.digitalRead(hall_sensor)):
            BP.reset_all()
            unloadCargo()
        time.sleep(0.5)
    
except KeyboardInterrupt:
    BP.reset_all()