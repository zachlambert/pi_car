# -*- coding: utf-8 -*-

import numpy as np
import cv2

from camera.camera import Camera, CameraServer
from utils.updater import Updater

class ObjectTracker:
    
    def __init__(self):
        self._low_range = (25, 70, 25)
        self._high_range= (80, 255, 255)
        self._correct_radius = 120
        self._centre = 160
        self._running = False
        
    def find_object(self, frame, draw_circle=False):
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        masked = cv2.inRange(frame_hsv, self._low_range, self._high_range)
        _, contours, _ = cv2.findContours(masked, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        
        largest_pos = (0, 0)
        largest_radius = 0
        
        for contour in contours:
            pos, radius = cv2.minEnclosingCircle(contour)    
            if radius > largest_radius:
                largest_radius = int(radius)
                largest_pos = (int(pos[0]), int(pos[1]))
            
        if largest_radius>0 and draw_circle:
            cv2.circle(frame, largest_pos, largest_radius, [0, 0, 255])
                
        return masked, largest_pos, largest_radius
    
    
def test():
    server = CameraServer()
    camera = Camera()
    tracker = ObjectTracker()
    
    def update(time):
        frame = camera.update()
        masked, pos, radius = tracker.find_object(frame, draw_circle=True)
        server.put_images(frame, masked)
    
    updater = Updater(0.01)
    updater.add(update)
    while updater.timer<120:
        updater.update()

    server.stop()
    
    
    