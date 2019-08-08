# -*- coding: utf-8 -*-
"""
Provides a servo class for setting up and controlling servos.

"""

import time

import RPi.GPIO as GPIO

from pin_data import get_pins


class Servo:
    
    def __init__(self, pins, start_angle=90, min_angle=0, max_angle=180):
        self.pins = pins
        self.angle = start_angle
        self.min_angle = min_angle
        self.max_angle = max_angle    
        self.frequency = 10
        
        GPIO.setup(self.pins.PWM, GPIO.OUT)
        self.servo_pwm = GPIO.PWM(self.pins.PWM, self.frequency)
        self.servo_pwm.start(self.angle_to_duty_cycle(self.angle))
        
    def angle_to_duty_cycle(self, angle):
        return (self.frequency/100) * (angle/10.0 + 2.5)
    
    def set_angle(self, angle):
        if angle<self.min_angle:
            angle = self.min_angle
        if angle>self.max_angle:
            angle = self.max_angle
            
        duty_cycle = self.angle_to_duty_cycle(angle)
        self.servo_pwm.ChangeDutyCycle(duty_cycle)
        

def test_servo():
    pins = get_pins()
    GPIO.setmode(GPIO.BOARD)

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
    GPIO.cleanup()