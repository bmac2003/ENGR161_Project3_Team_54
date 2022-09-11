# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 13:10:41 2021

@author: btmcl
"""
import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers

BP = brickpi3.BrickPi3()

try:
    while True:  
        BP.set_motor_power(BP.PORT_1, -10)
        time.sleep(1)
        BP.set_motor_power(BP.PORT_1, 10)
        time.sleep(1)
        
except KeyboardInterrupt:
    BP.reset_all()