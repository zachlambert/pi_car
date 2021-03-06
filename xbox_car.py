# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
from xbox import xbox

from mechanisms.car import Car
from mechanisms.camera_mount import CameraMount
from camera.camera import Camera, CameraServer
from camera.object_tracker import ObjectTracker
from pin_data import get_pins
from utils.updater import Updater


pins = get_pins()
GPIO.setmode(GPIO.BOARD)

car = Car(pins["car"])
camera_mount = CameraMount(pins["camera mount"])
camera = Camera()
camera_server = CameraServer()
tracker = ObjectTracker()

def update_camera(time):
    camera.update()
    frame = camera.update()
    masked, pos, radius = tracker.find_object(frame, draw_circle=True)
    camera_server.put_images(frame, masked)
    
updater = Updater(0)
updater.add(car.update)
updater.add(camera_mount.update)
updater.add(update_camera)

joy = xbox.Joystick()

while not joy.Back():
    if not joy.connected():
        car.set_velocities(0, 0)
    else:
        if joy.rightTrigger()>0.05:
            car.set_velocity(joy.rightTrigger()*30)
        elif joy.leftTrigger()>0.05:
            car.set_velocity(-joy.leftTrigger()*30)
        else:
            car.set_velocity(0)
            
        if abs(joy.leftX())>0.05:
            car.set_angular_velocity(joy.leftX()*90)
        else:
            car.set_angular_velocity(0)
            
        if abs(joy.rightX())>0.05:
            camera_mount.pan_servo.velocity = -joy.rightX()*120
        else:
            camera_mount.pan_servo.velocity = 0
            
        if abs(joy.rightY())>0.05:
            camera_mount.tilt_servo.velocity = -joy.rightY()*120
            
        else:
            camera_mount.tilt_servo.velocity = 0
            
    updater.update()

#camera_server.stop()
