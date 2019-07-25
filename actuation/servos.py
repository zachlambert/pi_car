"""
servos.py

Purpose: To provide a Servo class for controlling servos.

"""

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

class Servo:
    
    def __init__(self, PIN, start_angle=90, min_angle=0, max_angle=180):
        self.PIN = PIN
        self.angle = start_angle
        self.min_angle = min_angle
        self.max_angle = max_angle
        
        self.frequency = 35
        
        GPIO.setup(self.PIN, GPIO.OUT)
        self.servo_pwm = GPIO.PWM(self.PIN, self.frequency)
        self.servo_pwm.start(self.angleToDutyCycle(self.angle))
        
    def angleToDutyCycle(self, angle):
        return (self.frequency/100) * (angle/10.0 + 2.5)
    
    def setAngle(self, angle):
        if(angle<self.min_angle):
            angle = self.min_angle
        if(angle>self.max_angle):
            angle = self.max_angle
            
        duty_cycle = self.angleToDutyCycle(angle)
        self.servo_pwm.ChangeDutyCycle(duty_cycle)
        

if __name__ == "__main__":
    
    SERVO_1 = 10
    SERVO_2 = 12
    
    servo1 = Servo(SERVO_1)
    servo2 = Servo(SERVO_2)
    
    print("Testing servo 1")
    
    time.sleep(1)
    
    print("Angle: 0")
    servo1.setAngle(0)
    time.sleep(1)
    
    print("Angle: 90")
    servo1.setAngle(90)
    time.sleep(1)

    print("Angle: 180")
    servo1.setAngle(180)
    time.sleep(1)
    
    servo1.setAngle(90)    
    
    print("Testing servo 2")
    
    time.sleep(1)
    
    print("Angle: 0")
    servo2.setAngle(0)
    time.sleep(1)
    
    print("Angle: 90")
    servo2.setAngle(90)
    time.sleep(1)
    
    print("Angle: 180")
    servo2.setAngle(180)
    time.sleep(1)
    
    servo2.setAngle(90)
    
    print("Finished")
    GPIO.cleanup()