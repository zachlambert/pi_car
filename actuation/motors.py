"""
motors.py

Purpose: To provide classes and functions for controlling motors with the HW95
motor driver, reading encoders and coupling these together.

"""

import time

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

class HW95Motor:
    
    def __init__(self, IN1, IN2, EN, flip_dir=False):
        if not flip_dir:
            self.IN1 = IN1
            self.IN2 = IN2
        else:
            self.IN1 = IN2
            self.IN2 = IN1
            
        self.EN = EN
        
        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.EN, GPIO.OUT)
        
        GPIO.output(self.IN1, False)
        GPIO.output(self.IN2, False)
        
        self.en_pwm = GPIO.PWM(self.EN, 100) #100 Hz
        self.en_pwm.start(0) #Default to 0 duty cycle
        
    def setSpeed(self, speed_percentage):
        self.en_pwm.ChangeDutyCycle(0)
        
        if(speed_percentage>0):
            GPIO.output(self.IN1, True)
            GPIO.output(self.IN2, False)
        elif(speed_percentage<0):
            GPIO.output(self.IN1, False)
            GPIO.output(self.IN2, True)
        else:
            GPIO.output(self.IN1, False)
            GPIO.output(self.IN2, False)
            return
        
        magnitude = abs(speed_percentage)
        if(magnitude>100):
            magnitude = 100
            
        self.en_pwm.ChangeDutyCycle(magnitude)
       
        
#Functions for testing

def testMotors():
    
    GPIO.setmode(GPIO.BOARD)

    #Left motor
    HW95_IN1 = 11
    HW95_IN2 = 13
    HW95_ENA = 15
    #Right motor
    HW95_IN3 = 22
    HW95_IN4 = 24
    HW95_ENB = 26
    
    left_motor = HW95Motor(HW95_IN1, HW95_IN2, HW95_ENA, True)
    right_motor = HW95Motor(HW95_IN3, HW95_IN4, HW95_ENB, True)

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
    