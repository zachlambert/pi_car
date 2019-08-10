# -*- coding: utf-8 -*-
"""
Provides a LineFollower class, which uses a Car object to control the robot
and 2 OptoInterrupter objects to detect the line.

"""

import time

from mechanisms.car import Car
from sensors.opto_interrupter import OptoInterrupter


class LineFollower:
    
    def __init__(self, pins):
        self._car = Car(pins.car_pins)
        self._left_opto_interrupter = OptoInterrupter(
            pins.left_opto_interrupter_pins)
        self._right_opto_interrupter = OptoInterrupter(
            pins.right_opto_interrupter_pins)
        
        self._MAX_VELOCITY = 30
        self._MIN_VELOCITY = -10
        self._VELOCITY_DECAY_RATE = 200 #When turning, velocity decreases by 2cm/s per second
        self._MAX_ANGULAR_VELOCITY = 180
        self._MIN_ANGULAR_VELOCITY = 0
        self._ANGULAR_VELOCITY_GROW_RATE = 50
        self._velocity = self._MAX_VELOCITY    
        self._angular_velocity = 0
        self._turning_timer = 0
        self._direction = 0 #1 = clockwise, -1 = anticlockwise, 0 = straight
        self._prev_time = time.time()
        
    def update(self):
        self._car.update()
        
        current_time = time.time()
        elapsed_time = current_time - self._prev_time
        self._prev_time = current_time
        
        new_direction = 0
        if self._at_left_edge() and self._at_right_edge():
            self._car.set_velocities(-0.5, self._direction*30)
            return
        if self._at_left_edge():
            new_direction = 1
        elif self._at_right_edge():
            new_direction = -1
            
        if new_direction == self._direction:
            if new_direction == 1:
                self._turning_timer += elapsed_time
            elif new_direction == -1:
                self._turning_timer -= elapsed_time
        else:
            self._turning_timer = 0
            self._direction = new_direction
        
        self._velocity = self._MAX_VELOCITY \
            - abs(self._turning_timer) * self._VELOCITY_DECAY_RATE
        self._angular_velocity = \
                (self._MIN_ANGULAR_VELOCITY + self._MAX_ANGULAR_VELOCITY)/2 \
                 + (self._turning_timer
                    * self._ANGULAR_VELOCITY_GROW_RATE
                    * self._direction)
                
        if self._velocity < self._MIN_VELOCITY:
            self._velocity = self._MIN_VELOCITY
        elif self._velocity > self._MAX_VELOCITY:
            self._velocity = self._MAX_VELOCITY
        if self._angular_velocity < self._MIN_ANGULAR_VELOCITY:
            self._angular_velocity = self._MIN_ANGULAR_VELOCITY
        elif self._angular_velocity > self._MAX_ANGULAR_VELOCITY:
            self._angular_velocity = self._MAX_ANGULAR_VELOCITY
        
        self._angular_velocity *= self._direction
        self._car.set_velocities(self._velocity, self._angular_velocity)
        
    def _at_left_edge(self):
        return self._right_opto_interrupter.get_value() == 1
    
    def _at_right_edge(self):
        return self._left_opto_interrupter.get_value() == 1