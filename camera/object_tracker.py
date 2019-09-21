# -*- coding: utf-8 -*-

import numpy as np
import cv2


class ObjectTracker:
    
    def __init__(self):
        self._low_range = (25, 70, 25)
        self._high_range= (80, 255, 255)
        self._correct_radius = 120
        self._centre = 160
        self._running = False
        
    def find_object(self, frame):
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        masked = cv2.inRange(frame_hsv, self._low_range, self._high_range)
        contour_image = np.copy(masked)
        contours, _ = cv2.findContours(contour_image,
                                       cv2.REIR_LIST,
                                       cv2.CHAIN_APPROX_SIMPLE)
        circles = [cv2.minEnclosingCircle(contour) for contour in contours]
        
        largest_pos = (0, 0)
        largest_radius = 0
        for (x, y), radius in circles:
            if radius > largest_radius:
                largest_radius = int(radius)
                largest_pos = (int(x), int(y))
                
        return masked, largest_pos, largest_radius