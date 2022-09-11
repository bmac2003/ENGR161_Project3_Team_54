# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 14:00:35 2021

@author: btmcl
"""

import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class

speed = -30
count = 0

try:
    while True:
        while (count < 10):
            BP.set_motor_power(BP.PORT_A+BP.PORT_D, speed / 10 * count)
            time.sleep(0.05)
        print("AT MAX POWER")
        BP.set_motor_power(BP.PORT_A+BP.PORT_D, speed)
        time.sleep(20)
        BP.reset_all()
        
except KeyboardInterrupt:
    BP.reset_all()
