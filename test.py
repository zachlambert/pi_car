# -*- coding: utf-8 -*-
"""
Running this script prompts the user to select a module to test. This module
is then tested by running the appropriate test function.

"""

import importlib


_test_modules = {
    'motor': 'actuation.motor',
    'smart_motor': 'actuation.smart_motor',
    'servo': 'actuation.servo',
    'car': 'mechanisms.car',
    'encoder': 'sensors.encoder',
    'compass': 'sensors.compass',
    'mpu': 'sensors.mpu',
    'opto-interrupter': 'sensors.opto_interrupter',
    'camera': 'camera.camera'
}

running = True

while running:
    print("Enter name of component to test or type 'exit'")    
    name = input(">").strip()    
        
    if name in _test_modules:
        print("Running test program for ", name)
        print("")
        test_module = importlib.import_module(_test_modules[name])
        test_module.test()
        print("")
    elif name == "exit":
        running = False
        print("Exiting")
    else: 
        print("Invalid input")