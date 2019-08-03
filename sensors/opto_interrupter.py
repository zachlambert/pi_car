"""
opto_interrupter.py

Purspose: Provides class for interfacing with a opto-interrupter
module, for line following.

"""

import RPi.GPIO as GPIO
import time
from pin_data import getPins

GPIO.setmode(GPIO.BOARD)

class OptoInterrupter:
    
    def __init__(self, pins):
        self.pins = pins
        
        GPIO.setup(self.pins.OUT, GPIO.IN)
        
    def getValue(self):
        return GPIO.input(self.pins.OUT)
    
    
def testOptoInterrupter():
    
    GPIO.setmode(GPIO.BOARD)
    
    pins = getPins()
    
    left = OptoInterrupter(pins["left opto-interrupter"])
    right = OptoInterrupter(pins["right opto-interrupter"])
    
    print("Reading left opto-interrupter")
    
    time.sleep(1)
    
    end_time = time.time() + 5
    while time.time() < end_time:
        print(left.getValue())
        time.sleep(0.05)
        
    print("Reading right opto-interrupter")
    
    time.sleep(1)
    
    end_time = time.time() + 5
    while time.time() < end_time:
        print(right.getValue())
        time.sleep(0.05)
        
    time.sleep(1)
    
    print("Finished")
    
    GPIO.cleanup()