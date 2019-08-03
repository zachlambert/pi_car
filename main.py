import RPi.GPIO as GPIO
import time

from pin_data import getPins

from actuation.smart_motors import SmartMotor

print("Setup")

#Setup

pins = getPins()

GPIO.setmode(GPIO.BOARD)

#Motors

left_motor = SmartMotor(pins["left motor"], pins["left encoder"], 20, 3, True)
right_motor = SmartMotor(pins["right motor"], pins["right encoder"], 20, 3, True)

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
