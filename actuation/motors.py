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
    
    def __init__(self, PIN, num_slots, wheel_radius):
        self.PIN = PIN
        self.num_changes = num_slots*2
        self.wheel_radius = wheel_radius
        self.pulse_count = 0

        self.distance_step = self.wheel_radius * ((2*math.pi) / self.num_changes)
        self.speed = 0
        self.prev_time = time.time()
        self.change_list = []
        self.measure_window= 0.1
        
        GPIO.setup(self.PIN, GPIO.IN)
        
        GPIO.remove_event_detect(self.PIN)
        GPIO.add_event_detect(self.PIN, GPIO.BOTH, self.callback)
        
    def callback(self, channel):
        self.pulse_count += 1
        current_time = time.time()
        elapsed_time = current_time - self.prev_time
        self.prev_time = current_time
        
        i = 0
        while i < len(self.change_list):
            self.change_list[i] += elapsed_time
            if self.change_list[i] > self.measure_window:
                self.change_list.pop(i)
            else:
                i+=1
            
        self.change_list.append(0)
        
    def getSpeed(self):
        current_time = time.time()
        elapsed_time = current_time - self.prev_time
        time_limit = self.measure_window - elapsed_time
        
        change_count = 0
        for change in self.change_list:
            if change <= time_limit:
                change_count+=1
                
        return (change_count * self.distance_step) / self.measure_window
    
    def reset(self):
        self.pulse_count = 0

    def getDistance(self): #in cm
        return self.wheel_radius * (self.pulse_count/self.num_changes) * (2*math.pi)        
        
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
    
    
def testEncoders():
    
    GPIO.setmode(GPIO.BOARD)

    #Left motor
    HW95_IN1 = 11
    HW95_IN2 = 13
    HW95_ENA = 15
    #Right motor
    HW95_IN3 = 22
    HW95_IN4 = 24
    HW95_ENB = 26
    
    ENCODER_LEFT = 7
    ENCODER_RIGHT = 8
    
    left_motor = HW95Motor(HW95_IN1, HW95_IN2, HW95_ENA, True)
    right_motor = HW95Motor(HW95_IN3, HW95_IN4, HW95_ENB, True)
        
    left_encoder = WheelEncoder(ENCODER_LEFT, 20, 3)
    right_encoder = WheelEncoder(ENCODER_RIGHT, 20, 3)
    
    #Test left encoder
    
    print("Testing left encoder")
    
    time.sleep(1)
    
    print("Moving left motor 20cm")
    left_motor.setSpeed(50)
    
    left_encoder.reset()
    while left_encoder.getDistance()<20:
        time.sleep(0.01)
        
    left_motor.setSpeed(0)
    
    time.sleep(1)
    
    print("Measure the speed of the left motor")
    
    time.sleep(1)
    
    left_motor.setSpeed(50)
    
    end_time = time.time() + 1.5
    while time.time() < end_time:
        print(left_encoder.getSpeed())
        time.sleep(0.1)
        
    left_motor.setSpeed(0)

    #Test right encoder
    
    print("Testing right encoder")
    
    time.sleep(1)
    
    print("Moving right motor 20cm")
    right_motor.setSpeed(50)
    
    right_encoder.reset()
    while right_encoder.getDistance()<20:
        time.sleep(0.01)
        
    right_motor.setSpeed(0)
    
    time.sleep(1)
    
    print("Measure the speed of the right motor")
    
    time.sleep(1)
    
    right_motor.setSpeed(50)
    
    end_time = time.time() + 1.5
    while time.time() < end_time:
        print(right_encoder.getSpeed())
        time.sleep(0.1)
        
    right_motor.setSpeed(0)
    
    time.sleep(1)
    
    print("Finished")
    GPIO.cleanup()