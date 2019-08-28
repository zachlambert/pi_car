# -*- coding: utf-8 -*-
"""
Running this script prompts the user to select a module to test. This module
is then tested by running the appropriate test function.

"""

from actuation.motor import test_motor
from actuation.smart_motor import test_smart_motor
from actuation.servo import test_servo
from mechanisms.car import test_car
from sensors.encoder import test_encoder
from sensors.compass import test_compass
from sensors.mpu import test_mpu
from sensors.opto_interrupter import test_opto_interrupter


test_strings = ["motor", "smart motor", "servo", "car", "encoder", "compass", "mpu", "opto-interrupter"]
test_functions = [test_motor, test_smart_motor, test_servo, test_car, test_encoder, test_compass, test_mpu, test_opto_interrupter]

class Program:
    
    def __init__(self):
        pass
    
    def update(self, instruction):
        for i in range(len(test_strings)):
            if test_strings[i]==instruction:
                test_functions[i]()
                break
            
    def stop(self):
        pass