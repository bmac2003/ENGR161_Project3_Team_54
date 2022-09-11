# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 13:26:34 2021

@author: btmcl
"""

import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers
import grovepi  # import the GrovePi drivers

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class
LEFT_POWER = BP.PORT_A+BP.PORT_B  # Constants for which port each motor is attached
RIGHT_POWER = BP.PORT_C+BP.PORT_D # to so it is easier to adjust

# Connect the Grove Line Finder to digital port D7
# SIG,NC,VCC,GND
line_finderL = 7
line_finderR = 8
ultrasonic_ranger = 4
hall_sensor = 2
grovepi.pinMode(line_finderL,"INPUT")
grovepi.pinMode(line_finderR,"INPUT")

BP.offset_motor_encoder(BP.PORT_A, BP.get_motor_encoder(BP.PORT_A))
BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B))
BP.offset_motor_encoder(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C))
BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D))

def unloadCargo():
    BP.reset(BP.PORT_1)
    BP.set_motor_power(BP.PORT_A, 30)
    time.sleep(5)
    BP.set_motor_power(BP.PORT_A, -30)
    time.sleep(5)
    return

try:
    while True:
        BP.set_motor_power(BP.PORT_B+BP.PORT_C+BP.PORT_D,30)
        if (grovepi.ultrasonicRead(ultrasonic_ranger) < 10):
            BP.reset_all()
            #unloadCargo()
            break
        
except KeyboardInterrupt:
    BP.reset_all()