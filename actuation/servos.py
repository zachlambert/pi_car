"""
servos.py

Purpose: To provide a Servo class for controlling servos.

"""

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

class Servo:
    
    def __init__(self, PIN, start_angle=90, min_angle=0, max_angle=180):
        self.PIN = PIN
        self.angle = start_angle
        self.min_angle = min_angle
        self.max_angle = max_angle
        
        GPIO.setup(self.PIN, GPIO.OUT)
        self.servo_pwm = GPIO.PWM(self.PIN, 100)
        self.servo_pwm.start(self.angleToDutyCycle(self.angle))
        
    def angleToDutyCycle(angle):
        return (float(angle)/10.0) + 2.5
    
    def setAngle(self, angle):
        if(angle<self.min_angle):
            angle = self.min_angle
        if(angle>self.max_angle):
            angle = self.max_angle
            
        duty_cycle = self.angleToDutyCycle(angle)
        self.servo_pwm.ChangeDutyCycle(duty_cycle)