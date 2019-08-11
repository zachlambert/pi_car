# -*- coding: utf-8 -*-
"""
Provides a virtual Car and OptoInterrupter to pass to the virtual
LineFollower class

"""

import numpy as np


class Car:
    
    def __init__(self, x, y, angle):
        self.pos = np.array([x, y])
        self.angle = angle
        self.size = np.array([25, 15]) #Length against width

    def update():
        pass
    
    def set_velocities(self, velocity, angular_velocity):
        self.velocity = velocity
        self.angular_velocity = angular_velocity
        
class OptoInterrupter:
    
    def __init__(self, x_offset, y_offset):
        self._offset = np.array([x_offset, y_offset])
        self._pos = np.array(self._offset)
        self.radius = 2
        
    def set_position(self, car):
        c = np.cos(car.angle)
        s = np.sin(car.angle)
        rotation_matrix = np.array([[c, -s], [s, c]])
        self._pos = car.pos + rotation_matrix*self._offset
    
    def get_value():
        return 0 #todo