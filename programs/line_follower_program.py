# -*- coding: utf-8 -*-
"""
This script doesn't run a specific program.
It is used to run code to test certain modules, which will change as new
modules are written.
    
"""

import RPi.GPIO as GPIO

from mechanisms.line_follower import LineFollower
from utils.pin_data import get_pins


class Program:
    
    def __init__(self):
        pins = get_pins()
        GPIO.setmode(GPIO.BOARD)
        self.robot = LineFollower(pins["line follower"])
        self.running = True
        
    def update(self, instruction):
        if instruction=="stop":
            self.running=False
            self.robot._car.set_velocities(0, 0)
        elif self.running:
            self.robot.update()
            
    def stop(self):
        self.robot._car.set_velocities(0, 0)
        GPIO.cleanup()
