# -*- coding: utf-8 -*-
"""
Provides a SmartMotor class which uses negative feedback to set the speed
of a motor, using measurements from an encoder.

"""

import time

import RPi.GPIO as GPIO

from actuation.motor import HW95Motor
from control.pid_controller import PIDController
from pin_data import get_pins
from sensors.encoder import WheelEncoder


class SmartMotor:
    
    def __init__(self, motor_pins, encoder_pins, num_slots, wheel_radius, flip_dir=False):
        self._motor = HW95Motor(motor_pins, flip_dir)
        self._encoder = WheelEncoder(encoder_pins, num_slots, wheel_radius)        
        self._pid_controller = PIDController(0.16, 0.005, 0.03)        
        self._direction = 0
        self._target_speed = 0
        self.set_speed(0)
        
    def update(self):
        measured_speed = self._encoder.get_speed()
        motor_input = self._pid_controller.update(self._target_speed, measured_speed)        
        if motor_input > 100:
            motor_input = 100        
        if motor_input < 0:
            motor_input = 0        
        self._motor.set_speed(motor_input*self._direction)
        
    def set_speed(self, speed):
        if speed==0:
            self._direction = 0
            self._motor.set_speed(0)
            self._pid_controller.set_output(0)
        elif speed>0:
            self._direction = 1
        else:
            self._direction = -1            
        self._target_speed = abs(speed)

        
def test_smart_motor():
    GPIO.setmode(GPIO.BOARD)
    pins = get_pins()    
    left_motor = SmartMotor(pins["left motor"], pins["left encoder"], 20, 3, True)
    right_motor = SmartMotor(pins["right motor"], pins["right encoder"], 20, 3, True)
    
    print("Testing SmartMotor")    
    time.sleep(1)    
    print("Move forward in a straight line by giving the motors equal speeds")    
    left_motor.set_speed(15)
    right_motor.set_speed(15)    
    end_time = time.time() + 2
    while time.time() < end_time:
        left_motor.update()
        right_motor.update()
        time.sleep(0.01)    
    left_motor.set_speed(0)
    right_motor.set_speed(0)    
    time.sleep(1)
    
    print("Rotate on the spot by giving the motors opposite speeds")    
    left_motor.set_speed(15)
    right_motor.set_speed(-15)    
    end_time = time.time() + 2
    while time.time() < end_time:
        left_motor.update()
        right_motor.update()
        time.sleep(0.01)    
    left_motor.set_speed(0)
    right_motor.set_speed(0)    
    time.sleep(1)
    
    print("Varying the speed of left motor")
    start_speed = 0
    end_speed = 40
    start_time = time.time()
    end_time = start_time + 3
    while time.time() < end_time:
        elapsed_time = time.time() - start_time
        left_motor.set_speed(
            start_speed + (end_speed-start_speed)*(elapsed_time/3))
        left_motor.update()
        time.sleep(0.01)
    start_time = time.time()
    end_time = start_time + 3
    while time.time() < end_time:
        elapsed_time = time.time() - start_time
        left_motor.set_speed(
            end_speed - (end_speed-start_speed)*(elapsed_time/3))
        left_motor.update()
        time.sleep(0.01)
        
    print("Finished")
    GPIO.cleanup()