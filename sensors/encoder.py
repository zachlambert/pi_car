# -*- coding: utf-8 -*-
"""
Provides the WheelEncoder class for monitoring a wheel encoder.

"""

import math
import time

import RPi.GPIO as GPIO

from actuation.motor import HW95Motor 
from utils.pin_data import get_pins


class WheelEncoder:
    
    def __init__(self, pins, NUM_SLOTS, WHEEL_RADIUS):
        self._pins = pins
        self._NUM_CHANGES = NUM_SLOTS*2
        self._WHEEL_RADIUS = WHEEL_RADIUS
        self._pulse_count = 0
        self._DISTANCE_STEP = self._WHEEL_RADIUS * ((2*math.pi) / self._NUM_CHANGES)
        self._speed = 0
        self._prev_time = time.time()
        self._change_list = []
        self._MEASURE_WINDOW = 0.1
        
        GPIO.setup(self._pins.OUT, GPIO.IN)
        GPIO.remove_event_detect(self._pins.OUT) #If an event detect is present already
        GPIO.add_event_detect(self._pins.OUT, GPIO.BOTH, self._callback)
        
    def _callback(self, channel):
        self._pulse_count += 1
        current_time = time.time()
        elapsed_time = current_time - self._prev_time
        self._prev_time = current_time
        
        i = 0
        while i < len(self._change_list):
            self._change_list[i] += elapsed_time
            if self._change_list[i] > self._MEASURE_WINDOW:
                self._change_list.pop(i)
            else:
                i+=1
        self._change_list.append(0)
        
    def get_speed(self):
        current_time = time.time()
        elapsed_time = current_time - self._prev_time
        time_limit = self._MEASURE_WINDOW - elapsed_time
        
        change_count = 0
        for change in self._change_list:
            if change <= time_limit:
                change_count+=1
                
        return (change_count*self._DISTANCE_STEP) / self._MEASURE_WINDOW
    
    def reset(self):
        self._pulse_count = 0

    def get_distance(self): #in cm
        return self._pulse_count * self._DISTANCE_STEP  
    
        
def test_encoder():
    pins = get_pins()
    GPIO.setmode(GPIO.BOARD)
    
    left_motor = HW95Motor(pins["left motor"], True)
    right_motor = HW95Motor(pins["right motor"], True)        
    left_encoder = WheelEncoder(pins["left encoder"], 20, 3)
    right_encoder = WheelEncoder(pins["right encoder"], 20, 3)
        
    print("Testing left encoder")    
    time.sleep(1)    
    print("Moving left motor 20cm")
    left_motor.set_speed(50)    
    left_encoder.reset()
    while left_encoder.get_distance()<20:
        time.sleep(0.01)        
    left_motor.set_speed(0)    
    time.sleep(1)    
    print("Measure the speed of the left motor")    
    time.sleep(1)    
    left_motor.set_speed(50)    
    end_time = time.time() + 1.5
    while time.time() < end_time:
        print(left_encoder.get_speed())
        time.sleep(0.1)        
    left_motor.set_speed(0)
    
    print("Testing right encoder")    
    time.sleep(1)    
    print("Moving right motor 20cm")
    right_motor.set_speed(50)    
    right_encoder.reset()
    while right_encoder.get_distance()<20:
        time.sleep(0.01)        
    right_motor.set_speed(0)    
    time.sleep(1)    
    print("Measure the speed of the right motor")    
    time.sleep(1)    
    right_motor.set_speed(50)    
    end_time = time.time() + 1.5
    while time.time() < end_time:
        print(right_encoder.get_speed())
        time.sleep(0.1)        
    right_motor.set_speed(0)    
    time.sleep(1)
    
    print("Finished")
    GPIO.cleanup()