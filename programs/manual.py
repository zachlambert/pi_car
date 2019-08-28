# -*- coding: utf-8 -*-
"""
This script allows manual control of the robot by executing the following
commands:
    forward <distance>
    backward <distance>
    right <degrees>
    left <degrees>
    exit
    
"""

import time
import RPi.GPIO as GPIO

from mechanisms.car import Car
from utils.pin_data import get_pins
from sensors.mpu import Mpu
from utils.updater import Updater
from actuation.servo import Servo


class Program:
    
    def __init__(self):
        pins = get_pins()
        GPIO.setmode(GPIO.BOARD)
        
        self.car = Car(pins["car"])
        self.mpu = Mpu()
        self.pan_servo = Servo(pins["pan servo"])
        self.tilt_servo = Servo(pins["tilt servo"])
        self.pan_angle = 90
        self.tilt_angle = 90

        self.updater = Updater(0.01)
        self.updater.add(self.car.update)
        self.updater.add(self.mpu.update)
        
    def update(self, instruction):
        if instruction=="f":
            self.car.set_velocities(100, 0)
        elif instruction=="b":
            self.car.set_velocities(-100, 0)
        elif instruction=="l":
            self.car.set_velocities(0, 180)
        elif instruction=="r":
            self.car.set_velocities(0, -180)
        elif instruction=="s":
            self.car.set_velocities(0, 0)
        elif instruction=="cl":
            self.pan_angle += 15
            if self.pan_angle > 180:
                self.pan_angle = 180
            self.pan_servo.set_angle(self.pan_angle)
        elif instruction=="cr":
            self.pan_angle -= 15
            if self.pan_angle < 0:
                self.pan_angle = 0
            self.pan_servo.set_angle(self.pan_angle)
        elif instruction=="cd":
            self.tilt_angle += 15
            if self.tilt_angle > 180:
                self.tilt_angle = 180
            self.tilt_servo.set_angle(self.tilt_angle)
        elif instruction=="cu":
            self.tilt_angle -= 15
            if self.tilt_angle < 0:
                self.tilt_angle = 0
            self.tilt_servo.set_angle(self.tilt_angle)
            
        self.updater.update()
        
    def stop(self):
        pass #Stop program
