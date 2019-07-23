"""
motors.py

Purpose: To provide classes and functions for controlling motors with the HW95
motor driver, reading encoders and coupling these together.

"""

import math
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
            return
        
        magnitude = abs(speed_percentage)
        if(magnitude>100):
            magnitude = 100
            
        self.en_pwm.ChangeDutyCycle(magnitude)
       
        
class WheelEncoder:
    
    def __init__(self, PIN, num_slots, wheel_radius, extraCallback=None):
        self.PIN = PIN
        self.num_changes = num_slots*2
        self.wheel_radius = wheel_radius
        self.pulse_count = 0
        self.extraCallback = extraCallback
        
        self.distance_step = self.wheel_radius * ((2*math.pi) / self.num_changes)
        self.speed = 0
        self.prev_time = time.time()
        
        GPIO.setup(self.PIN, GPIO.IN)
        
        GPIO.add_event_detect(self.PIN, GPIO.BOTH, self.callback)

    def callback(self, channel):
        self.pulse_count += 1
        
        current_time = time.time()
        elapsed_time = current_time - self.prev_time
        self.prev_time = current_time
        self.speed = self.distance_step / elapsed_time
        
        if(self.extraCallback!=None):
            self.extraCallback()
        
    def resetCounter(self):
        self.pulse_count = 0

    def getSpeed(self):
        return self.distance_step

    def getDistance(self): #in cm
        return self.wheel_radius * (self.pulse_count/self.num_changes) * (2*math.pi)
    
    
class SmartWheel:
    
    def __init__(self, MOTOR_IN1, MOTOR_IN2, MOTOR_EN, ENCODER_PIN, num_slots, wheel_radius):
        self.motor = HW95Motor(MOTOR_IN1, MOTOR_IN2, MOTOR_EN)
        self.encoder = WheelEncoder(ENCODER_PIN, num_slots, wheel_radius, self.encoderCallback)
        self.target_speed = 0
        self.motor_input = 0
        self.measured_speed = 0
        self.kp = 0.5
        
    def updateMotorInput(self):
        error = self.target_speed - self.measured_speed
        self.motor_input += self.kp * error
        self.motor.setSpeed(self.motor_input)
        
    def setSpeed(self,target_speed):
        self.target_speed = target_speed
        self.updateMotorInput()
        
    def encoderCallback(self):
        self.measured_speed = self.encoder.getSpeed()
        self.updateMotorInput()
    