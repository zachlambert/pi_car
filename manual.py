# -*- coding: utf-8 -*-
"""
This script allows manual control of the robot by executing the following
commands:
    forward <distance>
    backward <distance>
    right <degrees>
    left <degrees>
    exit
    
"""

import RPi.GPIO as GPIO

from mechanisms.car import Car
from pin_data import get_pins
from sensors.mpu import Mpu
from utils.updater import Updater


pins = get_pins()
GPIO.setmode(GPIO.BOARD)

car = Car(pins["car"])
mpu = Mpu()
updater = Updater(0.01)
updater.add(car.update)
updater.add(mpu.update)

def run_car_until(condition_func):
    while not condition_func():
        updater.update()

def move_forward(distance):
    speed = 15
    car.set_velocities(speed,0)
    car.reset_distance()
    def condition_func():
        return car.distance > distance
    run_car_until(condition_func)
    car.set_velocities(0, 0)
    
    
def move_backward(distance):
    speed = 15
    car.set_velocities(-speed,0)
    car.reset_distance()
    def condition_func():
        return car.distance < -distance
    run_car_until(condition_func)
    car.set_velocities(0, 0)
    
    
def rotate_left(target_angle):
    angular_speed = 90
    car.set_velocities(0, -angular_speed)
    prev_angle = mpu.yaw
    angle_moved = 0
    def condition_func():
        nonlocal prev_angle, angle_moved
        angle = mpu.yaw
        angle_dif = angle - prev_angle
        prev_angle = angle
        if angle_dif<-5:
            angle_dif += 360
        angle_moved += angle_dif
        print("{} -> {}".format(angle_moved, target_angle))
        return angle_moved > target_angle - 1
    run_car_until(condition_func)
    car.set_velocities(0, 0)
    
    
def rotate_right(target_angle):
    angular_speed = 90
    car.set_velocities(0, angular_speed)
    prev_angle = mpu.yaw
    angle_moved = 0
    def condition_func():
        nonlocal prev_angle, angle_moved
        angle = mpu.yaw
        angle_dif = angle - prev_angle
        prev_angle = angle
        if angle_dif>5:
            angle_dif -= 360
        angle_moved += angle_dif
        return angle_moved < -target_angle + 1
    run_car_until(condition_func)
    car.set_velocities(0, 0)
    
    
def parse_int(string):
    try:
        integer = int(string)
        return integer
    except:
        print("Invalid integer")
        return 0
    
    
running = True
while running:
    
    print("Enter command:")
    user_input = input(">")
    words = user_input.split()
    
    if words[0] == "exit":
        print("Exiting")
        running = False        
    elif words[0] == "forward" or words[0]=="f":
        distance = parse_int(words[1])
        move_forward(distance)
    elif words[0] == "backward" or words[0]=="b":
        distance = parse_int(words[1])
        move_backward(distance)
    elif words[0] == "left" or words[0]=="l":
        angle = parse_int(words[1])
        rotate_left(angle)
    elif words[0] == "right" or words[0]=="r":
        angle = parse_int(words[1])
        rotate_right(angle)
    else:
        print("Command not recognised.")
    
