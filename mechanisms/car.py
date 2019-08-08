# -*- coding: utf-8 -*-
"""
Provides class for controlling a 2-wheel drive car, by setting the speed of
the two motors to match the velocity and angular velocity.

Velocity = Velocity of centre of car (cm/second)
Angular Velocity = Angular velocity of car, positive clockwise (radians/second)
Wheel Distance = Distance from car centre to either wheel (cm)

Left motor speed = Velocity + Wheel Distance * Angular Velocity
Right motor speed = Velocity - Wheel Distance ( Angular Velocity

Todo:
    Complete test function                                               

"""

import math

import RPi.GPIO as GPIO

from actuation.smart_motor import SmartMotor
from pin_data import get_pins


class Car:
    
    def __init__(self, pins):
        self.left_motor = SmartMotor(pins.left_motor_pins, pins.left_encoder_pins, 20, 3, True)
        self.right_motor = SmartMotor(pins.right_motor_pins, pins.right_encoder_pins, 20, 3, True)
        self.velocity = 0
        self.angular_velocity = 0 #clockwise
        self.wheel_distance = 6.2 #62cm from centre to either wheel
        
    def update(self):
        self.left_motor.update()
        self.right_motor.update()
        
    def update_motor_speeds(self):
        left_velocity = self.velocity + self.wheel_distance*self.angular_velocity
        right_velocity = self.velocity - self.wheel_distance*self.angular_velocity
        self.left_motor.set_speed(left_velocity)
        self.right_motor.set_speed(right_velocity)
        
    def set_velocities(self, velocity, angular_velocity):
        self.velocity = velocity
        self.angular_velocity = angular_velocity
        self.update_motor_speeds()
        
    def set_velocity(self, velocity):
        self.velocity = velocity
        self.update_motor_speeds()
        
    def set_angular_velocity(self, angular_velocity_degrees):
        self.angular_velocity = math.radians(angular_velocity_degrees)
        self.update_motor_speeds()
        
        
def test_car():
    GPIO.setmode(GPIO.BOARD)
    pins = get_pins()
    
    print("Test code for car is not implemented yet.")
    
    print("Finished")
    GPIO.cleanup()