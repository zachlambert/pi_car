"""
pid_controller.py

Purpose: Provides PIDController class for implementing PID control.

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
        self.kp = kp
        self.ki = ki
        self.kd = kd
        
        self.prev_time = time.time()
        self.prev_error = 0
        self.error_integral = 0
        
    def update(self, target, new_input):
        
        current_time = time.time()
        elapsed_time = current_time - self.prev_time
        self.prev_time = current_time
        
        new_error = target-new_input
        
        self.error_integral += self.prev_error * elapsed_time
        
        derivative = (new_error - self.prev_error) / elapsed_time
        
        output = self.kp*new_error
        output += self.ki*self.error_integral 
        output += self.kd*derivative
                 
        self.prev_error = new_error
                 
        return output
        
    
