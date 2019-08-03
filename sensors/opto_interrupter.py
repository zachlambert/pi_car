"""
opto_interrupter.py

Purspose: Provides class for interfacing with a opto-interrupter
module, for line following.

"""

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

class OptoInterrupter:
    
    def __init__(self, PIN):
        self.PIN = PIN
        
        GPIO.setup(self.PIN, GPIO.IN)
        
    def getValue(self):
        return GPIO.input(self.PIN)
    
    
def testOptoInterrupter():
    
    GPIO.setmode(GPIO.BOARD)

    left = OptoInterrupter(16)
    right = OptoInterrupter(18)
    
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