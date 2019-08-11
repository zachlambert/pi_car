# -*- coding: utf-8 -*-
"""
Runs a simulation of a line follower, using the same LineFollower class
as the physical robot, but replacing Car and OptoInterrupter with virtual
versions (with the same interfaces) which control a virtual robot.
The output is displayed simply using pygame.

"""

import numpy as np
import pygame



class LineFollower:
    
    def __init__(self, x, y, angle):
        self.pos = np.array([x, y])
        self.angle = angle
        self.size = np.array([25, 15]) #Length against width
        
        
def update():
        
def draw():
    
