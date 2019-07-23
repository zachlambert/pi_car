import RPi.GPIO as GPIO
import time
import math

from actuation.motors import HW95Motor, WheelEncoder 
from actuation.servos import Servo 

print("Setup")

#Setup

GPIO.setmode(GPIO.BOARD)

#Pins

HW95_IN1 = 11
HW95_IN2 = 13
HW95_ENA = 15
HW95_IN3 = 22
HW95_IN4 = 24
HW95_ENB = 26

ENCODER_LEFT = 7
ENCODER_RIGHT = 8

SERVO_1 = 10
SERVO_2 = 12

#Motor Driver

left_motor = HW95Motor(HW95_IN1, HW95_IN2, HW95_ENA, True)
right_motor = HW95Motor(HW95_IN3, HW95_IN4, HW95_ENB, True)

#Encoders

left_encoder = WheelEncoder(7, 20, 3.5)
right_encoder = WheelEncoder(8, 20, 3.5)
        
#Servos

servo1 = Servo(SERVO_1)
servo2 = Servo(SERVO_2)

servo1.setAngle(0)
servo2.setAngle(180)

time.sleep(1)

servo1.setAngle(180)
servo2.setAngle(0)   

time.sleep(1)

servo1.setAngle(90)
servo2.setAngle(90)

print("Starting main loop")

left_motor.setSpeed(50)
right_motor.setSpeed(50)

while left_encoder.getDistance()<5:
    time.sleep(0.005) 

print("Ending program")

left_motor.setSpeed(0)
right_motor.setSpeed(0)

GPIO.cleanup()
