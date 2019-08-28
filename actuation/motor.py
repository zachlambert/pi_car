# -*- coding: utf-8 -*-
"""
Provides classes and functions for controlling motors with the HW95
motor driver, reading encoders and coupling these together.

"""

import time

import RPi.GPIO as GPIO

from utils.pin_data import get_pins


class HW95Motor:
    
    def __init__(self, pins, flip_dir=False):
        self._pins = pins
        if flip_dir:
            self._pins.flip_direction()
            
        GPIO.setup(self._pins.IN1, GPIO.OUT)
        GPIO.setup(self._pins.IN2, GPIO.OUT)
        GPIO.setup(self._pins.EN, GPIO.OUT)
        self._en_pwm = GPIO.PWM(self._pins.EN, 100) #100 Hz
        
        GPIO.output(self._pins.IN1, False)
        GPIO.output(self._pins.IN2, False)
        self._en_pwm.start(0) #Default to 0 duty cycle
        
    def set_speed(self, speed_percentage):
        self._en_pwm.ChangeDutyCycle(0)
        
        if speed_percentage>0:
            GPIO.output(self._pins.IN1, True)
            GPIO.output(self._pins.IN2, False)
        elif speed_percentage<0:
            GPIO.output(self._pins.IN1, False)
            GPIO.output(self._pins.IN2, True)
        else:
            GPIO.output(self._pins.IN1, False)
            GPIO.output(self._pins.IN2, False)
            return
        
        magnitude = abs(speed_percentage)
        if magnitude>100:
            magnitude = 100
            
        self._en_pwm.ChangeDutyCycle(magnitude)
        

def test_motor():
    pins = get_pins()
    GPIO.setmode(GPIO.BOARD)
    left_motor = HW95Motor(pins["left motor"], True)
    right_motor = HW95Motor(pins["right motor"], True)

    print("Testing left motor")    
    time.sleep(1)    
    print("Left motor forward at 50%")
    left_motor.set_speed(50)
    time.sleep(1)    
    print("Left motor forward at 100%")
    left_motor.set_speed(100)
    time.sleep(1)
    print("Left motor stopping")
    left_motor.set_speed(0)
    time.sleep(1)    
    print("Left motor backward at 50%")
    left_motor.set_speed(-50)
    time.sleep(1)    
    print("Left motor backward at 100%")
    left_motor.set_speed(-100)
    time.sleep(1)
    left_motor.set_speed(0)
    
    print("Testing right motor")
    time.sleep(1)
    print("Right motor forward at 50%")
    right_motor.set_speed(50)
    time.sleep(1)    
    print("Right motor forward at 100%")
    right_motor.set_speed(100)
    time.sleep(1)
    print("Right motor stopping")
    right_motor.set_speed(0)
    time.sleep(1)
    print("Right motor backward at 50%")
    right_motor.set_speed(-50)
    time.sleep(1)    
    print("Right motor backward at 100%")
    right_motor.set_speed(-100)
    time.sleep(1)
    right_motor.set_speed(0)
    
    print("Finished")
    GPIO.cleanup()
    