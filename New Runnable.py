# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 15:39:14 2021

@author: btmcl
"""

import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers
import grovepi  # import the GrovePi drivers

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class
ultrasonic_ranger = 4

try:
    while True:
        BP.set_motor_power(BP.PORT_B+BP.PORT_C+BP.PORT_D,30)
        if (grovepi.ultrasonicRead(ultrasonic_ranger) < 10):
            BP.reset_all()
            
except KeyboardInterrupt:
    BP.reset_all()