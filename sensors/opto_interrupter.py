# -*- coding: utf-8 -*-
"""
Provides class for interfacing with a opto-interrupter
module, which will be used for line following.

"""

import time

import RPi.GPIO as GPIO

from utils.pin_data import get_pins


class OptoInterrupter:
    
    def __init__(self, pins):
        self._pins = pins        
        GPIO.setup(self._pins.OUT, GPIO.IN)
        
    def get_value(self):
        return GPIO.input(self._pins.OUT)
    
    
def test_opto_interrupter():    
    pins = get_pins()
    GPIO.setmode(GPIO.BOARD)    
    left = OptoInterrupter(pins["left opto-interrupter"])
    right = OptoInterrupter(pins["right opto-interrupter"])
    
    print("Reading left opto-interrupter")    
    time.sleep(1)    
    end_time = time.time() + 5
    while time.time() < end_time:
        print(left.get_value())
        time.sleep(0.05)        

    print("Reading right opto-interrupter")    
    time.sleep(1)    
    end_time = time.time() + 5
    while time.time() < end_time:
        print(right.get_value())
        time.sleep(0.05)        
    time.sleep(1)
    
    print("Finished")    
    GPIO.cleanup()