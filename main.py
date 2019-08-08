# -*- coding: utf-8 -*-
"""
This script doesn't run a specific program.
It is used to run code to test certain modules, which will change as new
modules are written.
    
"""

import time

import RPi.GPIO as GPIO

from mechanisms.car import Car
from pin_data import get_pins


print("Setup")
pins = get_pins()
GPIO.setmode(GPIO.BOARD)
car = Car(pins["car"])

print("Starting main loop")
car.set_velocities(15, 0)
end_time = time.time() + 2
while time.time()<end_time:
    car.update()
    time.sleep(0.01)
car.set_velocities(0, -2)
end_time = time.time() + 2
while time.time()<end_time:
    car.update()
    time.sleep(0.01)
car.set_velocities(-20, 1)
end_time = time.time() + 2
while time.time()<end_time:
    car.update()
    time.sleep(0.01)
    
print("Ending program")
car.set_velocities(0, 0)
GPIO.cleanup()
