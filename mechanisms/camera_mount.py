# -*- coding: utf-8 -*-

from actuation.servo import VelocityServo


class CameraMount:
    
    def __init__(self, pins):
        self.pan_servo = VelocityServo(pins.pan_servo_pins)
        self.tilt_servo = VelocityServo(pins.tilt_servo_pins,
                                        90, 20, 160)
        
    def update(self, dt):
        self.pan_servo.update(dt)
        self.tilt_servo.update(dt)
