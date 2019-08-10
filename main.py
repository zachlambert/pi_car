# -*- coding: utf-8 -*-
"""
This script doesn't run a specific program.
It is used to run code to test certain modules, which will change as new
modules are written.
    
"""

import time

import RPi.GPIO as GPIO

from mechanisms.line_follower import LineFollower
from pin_data import get_pins


pins = get_pins()
GPIO.setmode(GPIO.BOARD)
robot = LineFollower(pins["line follower"])

end_time = time.time() + 1000
while time.time()<end_time:
    robot.update()
    time.sleep(0.01)
    
robot._car.set_velocities(0, 0)
GPIO.cleanup()
