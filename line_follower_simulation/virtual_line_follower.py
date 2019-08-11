# -*- coding: utf-8 -*-
"""
Provides a LineFollower class, equivalent to the LineFollower used in the
physical robot, except that the car and opto_interrupter objects are passed
to the LineFollower in the constructor, where these objects are part of the
simulated world, but have the same interface as the classes for the physical
components.

"""

import time


class LineFollower:
    
    def __init__(self, world):
        self._world = world
        
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
        
    def update(self, elapsed_time):
        new_direction = 0
        if self._at_left_edge() and self._at_right_edge():
            self._world.set_car_velocities(-0.5, self._direction*30)
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
        self._world.set_car_velocities(self._velocity, self._angular_velocity)
                
    def _at_left_edge(self):
        return self._right_opto_interrupter.get_value() == 1
    
    def _at_right_edge(self):
        return self._left_opto_interrupter.get_value() == 1