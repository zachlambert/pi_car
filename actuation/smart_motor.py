# -*- coding: utf-8 -*-
"""
Provides a SmartMotor class which uses negative feedback to set the speed
of a motor, using measurements from an encoder.

"""

import time

import RPi.GPIO as GPIO

from actuation.motor import HW95Motor
from control.pid_controller import PIDController
from utils.pin_data import get_pins
from sensors.encoder import WheelEncoder
from utils.updater import Updater


class SmartMotor:
    
    def __init__(self, motor_pins, encoder_pins, num_slots, wheel_radius, flip_dir=False):
        self._motor = HW95Motor(motor_pins, flip_dir)
        self._encoder = WheelEncoder(encoder_pins, num_slots, wheel_radius)        
        self._pid_controller = PIDController(0.16, 0.005, 0.03)        
        self._direction = 0
        self._target_speed = 0
        self.set_velocity(0)
        
    def update(self, dt):
        measured_speed = self._encoder.get_speed()
        motor_input = self._pid_controller.update(self._target_speed, measured_speed, dt)        
        if motor_input > 100:
            motor_input = 100        
        if motor_input < 0:
            motor_input = 0        
        self._motor.set_speed(motor_input*self._direction)
        
    def set_velocity(self, speed):
        if speed==0:
            self._direction = 0
            self._motor.set_speed(0)
            self._pid_controller.set_output(0)
        elif speed>0:
            self._direction = 1
        else:
            self._direction = -1            
        self._target_speed = abs(speed)

    def get_velocity(self):
        return self._encoder.get_speed() * self._direction
        
def test_smart_motor():
    GPIO.setmode(GPIO.BOARD)
    pins = get_pins()    
    left_motor = SmartMotor(pins["left motor"], pins["left encoder"], 20, 3, True)
    right_motor = SmartMotor(pins["right motor"], pins["right encoder"], 20, 3, True)
    updater = Updater(0.01)
    updater.add(left_motor.update)
    updater.add(right_motor.update)
    
    print("Testing SmartMotor")    
    time.sleep(1)    
    print("Move forward in a straight line by giving the motors equal speeds")    
    left_motor.set_velocity(15)
    right_motor.set_velocity(15)
    updater.reset_timer()
    while updater.timer < 2:
        updater.update()
    left_motor.set_velocity(0)
    right_motor.set_velocity(0)    
    time.sleep(1)
    
    print("Rotate on the spot by giving the motors opposite speeds")    
    left_motor.set_velocity(15)
    right_motor.set_velocity(-15)    
    updater.reset_timer()
    while updater.timer < 2:
        updater.update()  
    left_motor.set_velocity(0)
    right_motor.set_velocity(0)    
    time.sleep(1)
    
    print("Varying the speed of left motor")
    start_speed = 0
    end_speed = 40
    updater.add(lambda dt: left_motor.set_velocity(
        start_speed + (end_speed-start_speed)*(updater.timer/3)))
    updater.reset_timer()
    while updater.timer < 3:
        updater.update()
    updater.remove(-1)
    updater.add(lambda dt: left_motor.set_velocity(
        end_speed - (end_speed-start_speed)*(updater.timer/3)))
    updater.reset_timer()
    while updater.timer < 3:
        updater.update()
    updater.remove(-1)
    left_motor.set_velocity(0)
    
    print("Finished")
    GPIO.cleanup()