# -*- coding: utf-8 -*-

import time

from server.image_app_core import start_server_process, get_control_instruction, put_output_image
from camera import pi_camera_stream
from pin_data import get_pins
from actuation.servo import Servo

pins = get_pins()
pan_servo = Servo(pins["pan servo"])
tilt_servo = Servo(pins["tilt servo"])
pan_angle = 90
tilt_angle = 90
ANGLE_CHANGE = 15

def update_pan(change):
    global pan_angle
    pan_angle += change
    if pan_angle < 0:
        pan_angle = 0
    if pan_angle > 180:
        pan_angle = 180
    pan_servo.set_angle(pan_angle)


def update_tilt(change):
    global tilt_angle
    tilt_angle += change
    if tilt_angle < 0:
        tilt_angle = 0
    if tilt_angle > 180:
        tilt_angle = 180
    tilt_servo.set_angle(tilt_angle)
    
    
def controlled_image_server_behaviour():
    camera = pi_camera_stream.setup_camera()
    time.sleep(0.1) # Allow camera to setup
    for frame in pi_camera_stream.start_stream(camera):
        encoded_bytes = pi_camera_stream.get_encoded_bytes_for_frame(frame)
        put_output_image(encoded_bytes)
        instruction = get_control_instruction()
        if instruction == "exit":
            print("Stopping")
            return
        elif instruction == "left":
            update_pan(ANGLE_CHANGE)
        elif instruction == "right":
            update_pan(-ANGLE_CHANGE)
        elif instruction == "down":
            update_tilt(ANGLE_CHANGE)
        elif instruction == "up":
            update_tilt(-ANGLE_CHANGE)
        
        
process = start_server_process("control_image_behaviour.html")
try:
    controlled_image_server_behaviour()
finally:
    process.terminate()