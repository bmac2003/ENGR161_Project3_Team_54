# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 16:35:35 2021

@author: btmcl
"""
import brickpi3 # import the BrickPi3 drivers
import time     # import the time library for the sleep function

BP = brickpi3.BrickPi3()

try:
    BP.set_motor_power(BP.PORT_A, 30)
    BP.set_motor_power(BP.PORT_D, -30)
    time.sleep(3)
    BP.reset_all()
    
except KeyboardInterrupt:
    BP.reset_all()
