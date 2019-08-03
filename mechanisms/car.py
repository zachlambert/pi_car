
from actuation.smart_motors import SmartMotor
import math

class Car:
    
    def __init__(self, pins):
        self.left_motor = SmartMotor(pins.left_motor_pins, pins.left_encoder_pins, 20, 3, True)
        self.right_motor = SmartMotor(pins.right_motor_pins, pins.right_encoder_pins, 20, 3, True)
        
        self.velocity = 0
        self.angular_velocity = 0 #clockwise
        self.wheel_distance = 6.2 #62cm from centre to either wheel
        
    def update(self):
        self.left_motor.update()
        self.right_motor.update()
        
    def updateMotorSpeeds(self):
        left_velocity = self.velocity + self.wheel_distance*self.angular_velocity
        right_velocity = self.velocity - self.wheel_distance*self.angular_velocity
        self.left_motor.setSpeed(left_velocity)
        self.right_motor.setSpeed(right_velocity)
        
    def setVelocities(self, velocity, angular_velocity):
        self.velocity = velocity
        self.angular_velocity = angular_velocity
        self.updateMotorSpeeds()
        
    def setVelocity(self, velocity):
        self.velocity = velocity
        self.updateMotorSpeeds()
        
    def setAngularVelocity(self, angular_velocity_degrees):
        self.angular_velocity = math.radians(angular_velocity_degrees)
        self.updateMotorSpeeds()