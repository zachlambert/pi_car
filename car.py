import RPi.GPIO as GPIO
import time
import math

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

GPIO.setup(HW95_IN1, GPIO.OUT)
GPIO.setup(HW95_IN2, GPIO.OUT)
GPIO.setup(HW95_ENA, GPIO.OUT)
hw95_enA_pwm = GPIO.PWM(HW95_ENA,100) #100 Hz

GPIO.setup(HW95_IN3, GPIO.OUT)
GPIO.setup(HW95_IN4, GPIO.OUT)
GPIO.setup(HW95_ENB, GPIO.OUT)
hw95_enB_pwm = GPIO.PWM(HW95_ENB,100) #100 Hz

#Encoders

class EncoderCounter(object):
    
    def __init__(self, pin_number, num_slots, wheel_radius):
        GPIO.setup(pin_number, GPIO.IN)
        self.pulse_count = 0
        self.pin_number = pin_number
        self.num_changes = num_slots*2
        self.wheel_radius = wheel_radius #in cm
        
        GPIO.add_event_detect(self.pin_number, GPIO.BOTH, self.callback)
        

    def callback(self, channel):
        self.pulse_count += 1
        
    def reset(self):
        self.current_value = GPIO.input(self.pin_number)
        self.pulse_count = 0

    def get_distance(self): #in cm
        return self.wheel_radius * (self.pulse_count/self.num_changes) * (2*math.pi)
    
left_encoder = EncoderCounter(7, 20, 3.5)

#Servos

GPIO.setup(SERVO_1, GPIO.OUT)
servo1_pwm = GPIO.PWM(SERVO_1, 100)
servo1_pwm.start(5)

GPIO.setup(SERVO_2, GPIO.OUT)
servo2_pwm = GPIO.PWM(SERVO_2, 100)
servo2_pwm.start(5)

def set_servo1_angle(angle):
    duty_cycle = (float(angle)/10.0) + 2.5
    servo1_pwm.ChangeDutyCycle(duty_cycle)

def set_servo2_angle(angle):
    duty_cycle = (float(angle)/10.0) + 2.5
    servo2_pwm.ChangeDutyCycle(duty_cycle)

set_servo1_angle(0)
set_servo2_angle(180)

time.sleep(1)

set_servo1_angle(180)
set_servo2_angle(0)   

time.sleep(1)

set_servo1_angle(90)
set_servo2_angle(90)

print("Starting main loop")

GPIO.output(HW95_IN1, True)
GPIO.output(HW95_IN2, False)
GPIO.output(HW95_IN3, True)
GPIO.output(HW95_IN4, False)

hw95_enA_pwm.start(50) #50% duty cycle
hw95_enB_pwm.start(50)

while left_encoder.get_distance()<5:
    time.sleep(0.005) 

print("Ending program")

hw95_enA_pwm.stop()
hw95_enB_pwm.stop()

servo1_pwm.stop()
servo2_pwm.stop()

GPIO.cleanup()
