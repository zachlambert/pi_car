# -*- coding: utf-8 -*-
"""
Provides class for controlling a 2-wheel drive car, by setting the speed of
the two motors to match the velocity and angular velocity.

Velocity = Velocity of centre of car (cm/second)
Angular Velocity = Angular velocity of car, positive clockwise (radians/second)
Wheel Distance = Distance from car centre to either wheel (cm)

Left motor speed = Velocity + Wheel Distance * Angular Velocity
Right motor speed = Velocity - Wheel Distance ( Angular Velocity

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
        self.velocity = 0
        self.angular_velocity = 0 #clockwise
        self._WHEEL_DISTANCE = 6.2 #62cm from centre to either wheel
        
        self.distance = 0
        
    def update(self, dt):
        self._left_motor.update()
        self._right_motor.update()
        measured_velocity = (self._left_motor.get_velocity()
                             + self._right_motor.get_velocity()) / 2     
        self.distance += dt * measured_velocity
        
    def reset_distance(self):
        self.distance = 0
        
    def set_velocities(self, velocity, angular_velocity_degrees):
        self.velocity = velocity
        self.angular_velocity = math.radians(angular_velocity_degrees)
        left_velocity = self.velocity + self._WHEEL_DISTANCE*self.angular_velocity
        right_velocity = self.velocity - self._WHEEL_DISTANCE*self.angular_velocity
        self._left_motor.set_velocity(left_velocity)
        self._right_motor.set_velocity(right_velocity)
        
        
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
    print("Rotating on the spot at 90 degrees per second")
    car.set_velocities(0, -90)
    end_time = time.time() + 2
    while time.time()<end_time:
        car.update()
        time.sleep(0.01)
    print("Reversing and turning left with turning radius 20cm")
    car.set_velocities(-20, math.degrees(1))
    end_time = time.time() + 2
    while time.time()<end_time:
        car.update()
        time.sleep(0.01)
    car.set_velocities(0, 0)
    
    print("Finished")
    GPIO.cleanup()