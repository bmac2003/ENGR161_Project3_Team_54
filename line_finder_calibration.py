# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 22:25:23 2021

@author: btmcl
"""

import grovepi  # import the GrovePi drivers
import time

line_finder = 2
grovepi.pinMode(line_finder,"INPUT")

try:
    while True:
        print(grovepi.digitalRead(line_finder))
        time.sleep(0.05)
        
except KeyboardInterrupt:
    print("EXIT")
