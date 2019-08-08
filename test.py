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
from sensors.opto_interrupter import test_opto_interrupter


test_strings = ["motor", "smart motor", "servo", "car", "encoder", "compass", "opto-interrupter"]
test_functions = [test_motor, test_smart_motor, test_servo, test_car, test_encoder, test_compass, test_opto_interrupter]
running = True

while running:
    print("Enter name of component to test or type 'exit'")    
    user_input = input(">").strip()    
    found = False    
    i = 0
    while i < len(test_strings):
        if test_strings[i] == user_input:
            found=True
            break
        i+=1
        
    if found:
        print("Running test program for ", test_strings[i])
        print("")
        test_functions[i]()
        print("")
    elif user_input == "exit":
        running = False
        print("Exiting")
    else: 
        print("Invalid input")