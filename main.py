import RPi.GPIO as GPIO
import time

from pin_data import getPins

from mechanisms.car import Car

print("Setup")

#Setup

pins = getPins()

GPIO.setmode(GPIO.BOARD)

#Motors

car = Car(pins["car"])

print("Starting main loop")

car.setVelocities(15, 0)

end_time = time.time() + 2
while time.time()<end_time:
    car.update()
    time.sleep(0.01)

car.setVelocities(0, -2)

end_time = time.time() + 2
while time.time()<end_time:
    car.update()
    time.sleep(0.01)
    
car.setVelocities(-20, 1)

end_time = time.time() + 2
while time.time()<end_time:
    car.update()
    time.sleep(0.01)
    
print("Ending program")

car.setVelocities(0, 0)

GPIO.cleanup()
