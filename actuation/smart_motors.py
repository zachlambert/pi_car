
from actuation.motors import HW95Motor
from sensors.encoders import WheelEncoder
from control.pid_controller import PIDController

import RPi.GPIO as GPIO
import time
    
class SmartMotor:
    
    def __init__(self, MOTOR_IN1, MOTOR_IN2, MOTOR_EN, ENCODER_PIN, num_slots, wheel_radius, flip_dir=False):
        self.motor = HW95Motor(MOTOR_IN1, MOTOR_IN2, MOTOR_EN, flip_dir)
        self.encoder = WheelEncoder(ENCODER_PIN, num_slots, wheel_radius)
        
        self.pid_controller = PIDController(0.16, 0.005, 0.03)
        
        self.direction = 0
        self.target_speed = 0

        self.setSpeed(0)
        
    def update(self):

        measured_speed = self.encoder.getSpeed()
        
        motor_input = self.pid_controller.update(self.target_speed, measured_speed)
        
        if motor_input > 100:
            motor_input = 100
        
        if motor_input < 0:
            motor_input = 0
        
        self.motor.setSpeed(motor_input*self.direction)

        
    def setSpeed(self, speed):
        if speed==0:
            self.direction = 0
        elif speed>0:
            self.direction = 1
        else:
            self.direction = -1
            
        self.target_speed = abs(speed)
        self.pid_controller.setOutput(100)
        self.motor.setSpeed(100*self.direction)
        
        
        
def testSmartMotors():
        
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
    
    left_motor = SmartMotor(HW95_IN1, HW95_IN2, HW95_ENA, ENCODER_LEFT, 20, 3, True)
    right_motor = SmartMotor(HW95_IN3, HW95_IN4, HW95_ENB, ENCODER_RIGHT, 20, 3, True)
    
    print("Testing SmartMotor")
    
    time.sleep(1)
    
    print("Move forward in a straight line by giving the motors equal speeds")
    
    left_motor.setSpeed(15)
    right_motor.setSpeed(15)
    
    end_time = time.time() + 4
    while time.time() < end_time:
        left_motor.update()
        right_motor.update()
        time.sleep(0.01)
    
    left_motor.setSpeed(0)
    right_motor.setSpeed(0)
    
    time.sleep(1)
    
    print("Rotate on the spot by giving the motors opposite speeds")
    
    left_motor.setSpeed(15)
    right_motor.setSpeed(-15)
    
    end_time = time.time() + 4
    while time.time() < end_time:
        left_motor.update()
        right_motor.update()
        time.sleep(0.01)
    
    left_motor.setSpeed(0)
    right_motor.setSpeed(0)
    
    time.sleep(1)
    
    print("Finished")
    GPIO.cleanup()