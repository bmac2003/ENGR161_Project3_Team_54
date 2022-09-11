# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 13:40:22 2021

@author: btmcl
"""

import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers
import grovepi  # import the GrovePi drivers

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class

hall_sensor = 1
ultrasonic_ranger = 6

BP.set_motor_power(BP.PORT_A+BP.PORT_D, -30)

try:
    while True:
        print("Hall Sensor Value: ", grovepi.digitalRead(hall_sensor))
        time.sleep(0.1)
        
        if (grovepi.ultrasonicRead(ultrasonic_ranger) < 20): #Stop if seeing something within range
            print("Too Close")
            while (grovepi.ultrasonicRead(ultrasonic_ranger) < 20):  #Stay stopped until obstacle moves
                BP.reset_all()
        
except KeyboardInterrupt:
    BP.reset_all()