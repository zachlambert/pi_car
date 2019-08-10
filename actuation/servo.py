# -*- coding: utf-8 -*-
"""
Provides a servo class for setting up and controlling servos.

"""

import time

import pigpio

from pin_data import get_pins


class Servo:
    
    def __init__(self, pins, start_angle=90, MIN_ANGLE=0, MAX_ANGLE=180):
        self._pins = pins
        self._angle = start_angle
        self._MIN_ANGLE = MIN_ANGLE
        self._MAX_ANGLE = MAX_ANGLE    
        self._pigpio_pi = pigpio.pi()
        self._update_duty_cycle()
        
    def _update_duty_cycle(self):
        #500 = 0 deg, 2500 = 180 deg
        duty_cycle = 500 + 2000*(self._angle/180)
        self._pigpio_pi.set_servo_pulsewidth(self._pins.PWM,
                                             duty_cycle)
    
    def set_angle(self, angle):
        if angle<self._MIN_ANGLE:
            angle = self._MIN_ANGLE
        if angle>self._MAX_ANGLE:
            angle = self._MAX_ANGLE
        self._angle = angle
        self._update_duty_cycle()
        

def test_servo():
    pins = get_pins()

    servo1 = Servo(pins["pan servo"])
    servo2 = Servo(pins["tilt servo"])
    
    print("Testing servo 1")
    time.sleep(1)    
    print("Angle: 0")
    servo1.set_angle(0)
    time.sleep(1)    
    print("Angle: 90")
    servo1.set_angle(90)
    time.sleep(1)
    print("Angle: 180")
    servo1.set_angle(180)
    time.sleep(1)    
    servo1.set_angle(90)    
    
    print("Testing servo 2")    
    time.sleep(1)    
    print("Angle: 0")
    servo2.set_angle(0)
    time.sleep(1)    
    print("Angle: 90")
    servo2.set_angle(90)
    time.sleep(1)    
    print("Angle: 180")
    servo2.set_angle(180)
    time.sleep(1)
    servo2.set_angle(90)
    
    print("Finished")