# -*- coding: utf-8 -*-
"""
Provides the WheelEncoder class for monitoring a wheel encoder.

"""

import math
import time

import RPi.GPIO as GPIO

from actuation.motor import HW95Motor 
from pin_data import get_pins


class WheelEncoder:
    
    def __init__(self, pins, num_slots, wheel_radius):
        self.pins = pins
        self.num_changes = num_slots*2
        self.wheel_radius = wheel_radius
        self.pulse_count = 0
        self.distance_step = self.wheel_radius * ((2*math.pi) / self.num_changes)
        self.speed = 0
        self.prev_time = time.time()
        self.change_list = []
        self.measure_window= 0.1
        
        GPIO.setup(self.pins.OUT, GPIO.IN)
        GPIO.remove_event_detect(self.pins.OUT)
        GPIO.add_event_detect(self.pins.OUT, GPIO.BOTH, self.callback)
        
    def callback(self, channel):
        self.pulse_count += 1
        current_time = time.time()
        elapsed_time = current_time - self.prev_time
        self.prev_time = current_time
        
        i = 0
        while i < len(self.change_list):
            self.change_list[i] += elapsed_time
            if self.change_list[i] > self.measure_window:
                self.change_list.pop(i)
            else:
                i+=1
        self.change_list.append(0)
        
    def get_speed(self):
        current_time = time.time()
        elapsed_time = current_time - self.prev_time
        time_limit = self.measure_window - elapsed_time
        
        change_count = 0
        for change in self.change_list:
            if change <= time_limit:
                change_count+=1
                
        return (change_count*self.distance_step) / self.measure_window
    
    def reset(self):
        self.pulse_count = 0

    def get_distance(self): #in cm
        return self.wheel_radius * (self.pulse_count/self.num_changes) * (2*math.pi)     
    
        
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