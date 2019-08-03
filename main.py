import RPi.GPIO as GPIO
import time

from actuation.smart_motors import SmartMotor

print("Setup")

#Setup

GPIO.setmode(GPIO.BOARD)

#Pins

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

SERVO_1 = 10
SERVO_2 = 12

#Motors

left_motor = SmartMotor(HW95_IN1, HW95_IN2, HW95_ENA, ENCODER_LEFT, 20, 3, True)
right_motor = SmartMotor(HW95_IN3, HW95_IN4, HW95_ENB, ENCODER_RIGHT, 20, 3, True)

print("Starting main loop")

left_motor.setSpeed(15)
right_motor.setSpeed(15)

end_time = time.time() + 3
while time.time()<end_time:
    left_motor.update()
    right_motor.update()
    time.sleep(0.01)

    
print("Ending program")

left_motor.setSpeed(0)
right_motor.setSpeed(0)

GPIO.cleanup()
