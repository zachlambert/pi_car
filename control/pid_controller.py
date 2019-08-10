# -*- coding: utf-8 -*-
"""
This module provides the PIDController class for implementing PID control.

The PID controller will take one input and produce an output.
This will be done by calling an update function, which takes the current input,
the desired input and returns the current output.

Differentiation will use a single-sided estimate.
deriative = (current error - previous error) / (time since previous)

Integration will use euler integration
integral = prev_integral + prev_error * (time since previous)

The output is computed as:
Output = kp*error + ki*integral + kd*derivative

"""

import time


class PIDController:
    
    def __init__(self, kp, ki, kd):
        self._kp = kp
        self._ki = ki
        self._kd = kd        
        self._prev_time = time.time()
        self._prev_error = 0
        self._error_integral = 0        
        self._output=0
        
    def update(self, target, new_input):
        current_time = time.time()
        elapsed_time = current_time - self._prev_time
        self._prev_time = current_time
        
        new_error = target-new_input
        self._error_integral += self._prev_error*elapsed_time
        derivative = (new_error-self._prev_error) / elapsed_time
        
        self._output += self._kp*new_error
        self._output += self._ki*self._error_integral 
        self._output += self._kd*derivative                 
        self._prev_error = new_error
        
        return self._output
        
    def set_output(self, output):
        self._output = output
