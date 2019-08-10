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
import time

import RPi.GPIO as GPIO

from actuation.smart_motor import SmartMotor
from pin_data import get_pins


class Car:
    
    def __init__(self, pins):
        self._left_motor = SmartMotor(pins.left_motor_pins, pins.left_encoder_pins, 20, 3, True)
        self._right_motor = SmartMotor(pins.right_motor_pins, pins.right_encoder_pins, 20, 3, True)
        self._velocity = 0
        self._angular_velocity = 0 #clockwise
        self._WHEEL_DISTANCE = 6.2 #62cm from centre to either wheel
        
    def update(self):
        self._left_motor.update()
        self._right_motor.update()
        
    def _update_motor_speeds(self):
        left_velocity = self._velocity + self._WHEEL_DISTANCE*self._angular_velocity
        right_velocity = self._velocity - self._WHEEL_DISTANCE*self._angular_velocity
        self._left_motor.set_speed(left_velocity)
        self._right_motor.set_speed(right_velocity)
        
    def set_velocities(self, velocity, angular_velocity):
        self._velocity = velocity
        self._angular_velocity = angular_velocity
        self._update_motor_speeds()
        
    def set_velocity(self, velocity):
        self._velocity = velocity
        self._update_motor_speeds()
        
    def set_angular_velocity(self, angular_velocity_degrees):
        self._angular_velocity = math.radians(angular_velocity_degrees)
        self._update_motor_speeds()
        
        
def test_car():
    GPIO.setmode(GPIO.BOARD)
    pins = get_pins()
    car = Car(pins["car"])
    
    print("Moving straight forward")
    car.set_velocities(15, 0)
    end_time = time.time() + 2
    while time.time()<end_time:
        car.update()
        time.sleep(0.01)
    print("Rotating on the spot")
    car.set_velocities(0, -2)
    end_time = time.time() + 2
    while time.time()<end_time:
        car.update()
        time.sleep(0.01)
    print("Reversing and turning left with turning radius 20cm")
    car.set_velocities(-20, 1)
    end_time = time.time() + 2
    while time.time()<end_time:
        car.update()
        time.sleep(0.01)
    car.set_velocities(0, 0)
    
    print("Finished")
    GPIO.cleanup()