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
        if self.extraCallback!=None:
            self.extraCallback()
            
    def reset(self):
        self.pulse_count = 0

    def getDistance(self): #in cm
        return self.wheel_radius * (self.pulse_count/self.num_changes) * (2*math.pi)
    
    
class SmartMotor:
    
    def __init__(self, MOTOR_IN1, MOTOR_IN2, MOTOR_EN, ENCODER_PIN, num_slots, wheel_radius, flip_dir=False):
        self.motor = HW95Motor(MOTOR_IN1, MOTOR_IN2, MOTOR_EN, flip_dir)
        self.encoder = WheelEncoder(ENCODER_PIN, num_slots, wheel_radius, self.encoderCallback)
        
        self.direction = 0
        
        self.prev_time = time.time()
        self.measured_speed = 0
        self.callback_count = 0
        self.callback_required = 2
        
        self.target_speed = 0
        self.error = 0
        self.motor_input = 0
        
        self.kp = 1.2
        self.ki = 0.1
        self.kd = 0.1
        
        self.setSpeed(0)
    
    def updateMotorInput(self, elapsed_time):
        print("Target: ", self.target_speed)
        print("Measured: ", self.measured_speed)
        prev_motor_input = self.motor_input
        
        new_error = self.target_speed - self.measured_speed
        self.motor_input += self.kp * new_error
        self.motor_input += self.ki * ((new_error - self.error)*elapsed_time)
        self.motor_input += self.kd * ((new_error - self.error)/elapsed_time)
        self.error = new_error
        
        print("Output: ", prev_motor_input, " to ", self.motor_input)
        
        if self.motor_input > 100:
            self.motor_input = 100
        
        if self.motor_input < 0:
            self.motor_input = 0
        
        self.motor.setSpeed(self.motor_input*self.direction)
        
        print("----")
        
    def setSpeed(self, speed):
        if speed==0:
            self.direction = 0
        elif speed>0:
            self.direction = 1
        else:
            self.direction = -1
            
        self.target_speed = abs(speed)
        self.motor_input = 100
        self.motor.setSpeed(self.motor_input*self.direction)
        
    def encoderCallback(self):
        self.callback_count += 1
        
        if self.callback_count>=self.callback_required:
            self.callback_count = 0
            
            current_time = time.time()
            elapsed_time = current_time - self.prev_time
            self.prev_time = current_time
            
            self.measured_speed = self.encoder.getDistance()/elapsed_time
            self.encoder.reset()
            
            self.updateMotorInput(elapsed_time)
        