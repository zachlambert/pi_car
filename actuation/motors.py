"""
motors.py

Purpose: To provide classes and functions for controlling motors with the HW95
motor driver, reading encoders and coupling these together.

"""

import time
from pin_data import getPins
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

class HW95Motor:
    
    def __init__(self, pins, flip_dir=False):
        self.pins = pins
        
        if flip_dir:
            pins.flipDirection()
        
        GPIO.setup(self.pins.IN1, GPIO.OUT)
        GPIO.setup(self.pins.IN2, GPIO.OUT)
        GPIO.setup(self.pins.EN, GPIO.OUT)
        
        GPIO.output(self.pins.IN1, False)
        GPIO.output(self.pins.IN2, False)
        
        self.en_pwm = GPIO.PWM(self.pins.EN, 100) #100 Hz
        self.en_pwm.start(0) #Default to 0 duty cycle
        
    def setSpeed(self, speed_percentage):
        self.en_pwm.ChangeDutyCycle(0)
        
        if(speed_percentage>0):
            GPIO.output(self.pins.IN1, True)
            GPIO.output(self.pins.IN2, False)
        elif(speed_percentage<0):
            GPIO.output(self.pins.IN1, False)
            GPIO.output(self.pins.IN2, True)
        else:
            GPIO.output(self.pins.IN1, False)
            GPIO.output(self.pins.IN2, False)
            return
        
        magnitude = abs(speed_percentage)
        if(magnitude>100):
            magnitude = 100
            
        self.en_pwm.ChangeDutyCycle(magnitude)
       
        
#Functions for testing

def testMotors():
    
    pins = getPins()
    
    GPIO.setmode(GPIO.BOARD)

    left_motor = HW95Motor(pins["left motor"], True)
    right_motor = HW95Motor(pins["right motor"], True)

    #Test left motor
    
    print("Testing left motor")
    
    time.sleep(1)
    
    print("Left motor forward at 50%")
    left_motor.setSpeed(50)
    time.sleep(1)
    
    print("Left motor forward at 100%")
    left_motor.setSpeed(100)
    time.sleep(1)
    

    print("Left motor stopping")
    left_motor.setSpeed(0)
    time.sleep(1)
    
    print("Left motor backward at 50%")
    left_motor.setSpeed(-50)
    time.sleep(1)
    
    print("Left motor backward at 100%")
    left_motor.setSpeed(-100)
    time.sleep(1)
    
    left_motor.setSpeed(0)
    
    #Test right motor
    
    print("Testing right motor")
    
    time.sleep(1)
    
    print("Right motor forward at 50%")
    right_motor.setSpeed(50)
    time.sleep(1)
    
    print("Right motor forward at 100%")
    right_motor.setSpeed(100)
    time.sleep(1)
    

    print("Right motor stopping")
    right_motor.setSpeed(0)
    time.sleep(1)
    
    print("Right motor backward at 50%")
    right_motor.setSpeed(-50)
    time.sleep(1)
    
    print("Right motor backward at 100%")
    right_motor.setSpeed(-100)
    time.sleep(1)
    
    right_motor.setSpeed(0)
    
    print("Finished")
    GPIO.cleanup()
    