"""
colour_detector.py

Purpose: Provides a class for controlling the colour sensor module

"""

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

RED_MIN = 10
RED_MAX = 40
GREEN_MIN = 20
GREEN_MAX = 40
BLUE_MIN = 10
BLUE_MAX = 40

class ColourDetector:
    
    def __init__(self, S0, S1, S2, S3, OUT):
        self.S0 = S0
        self.S1 = S1
        self.S2 = S2
        self.S3 = S3
        self.OUT = OUT
        
        self.pulse_time = 0
        self.pulse_read = False
        
        GPIO.setup(self.S0, GPIO.OUT)
        GPIO.setup(self.S1, GPIO.OUT)
        GPIO.setup(self.S2, GPIO.OUT)
        GPIO.setup(self.S3, GPIO.OUT)
        GPIO.setup(self.OUT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        #S0 and S1 control the pulse train frequency
        GPIO.output(self.S0, True)
        GPIO.output(self.S1, False)
        
    def timePulse(self):
        
        GPIO.wait_for_edge(self.OUT, GPIO.FALLING)
        
        start_time = time.time()

        GPIO.wait_for_edge(self.OUT, GPIO.RISING)
        
        end_time = time.time()
        
        return round((end_time - start_time) * 1e6, 0)
    
    def pulseToValue(self, pulse_time, min_value, max_value):
        
        if pulse_time<min_value:
            pulse_time = min_value
            
        if pulse_time>max_value:
            pulse_time = max_value
            
        #Min pulse time -> 255
        #Max pulse time -> 0
        return 255 * (max_value - pulse_time)/(max_value - min_value)
            
    def readColour(self, S2_value, S3_value, min_value, max_value):
        
        GPIO.output(self.S2, S2_value)
        GPIO.output(self.S3, S3_value)
        
        end_time = time.time() + 2
        while time.time() < end_time:
            print(GPIO.input(self.OUT))
    
        return 0            
        
        pulse_time = self.timePulse()
        print(pulse_time)
        value = self.pulseToValue(pulse_time, min_value, max_value)
        
        return value
    
    def readRed(self):
        return self.readColour(False, False, RED_MIN, RED_MAX)

    def readGreen(self):
        return self.readColour(True, True, GREEN_MIN, GREEN_MAX)

    def readBlue(self):
        return self.readColour(False, True, BLUE_MIN, BLUE_MAX)

if __name__ == "__main__":
    
    COLOUR_S0 = 18
    COLOUR_S1 = 19
    COLOUR_S2 = 21
    COLOUR_S3 = 23
    COLOUR_OUT = 16
    
    colour_detector = ColourDetector(COLOUR_S0, COLOUR_S1, COLOUR_S2, COLOUR_S3, COLOUR_OUT)
    
    end_time = time.time() + 8
    
    while time.time()<end_time:
        
        red = colour_detector.readRed()
        #blue = colour_detector.readBlue()
        #green = colour_detector.readGreen()
        
        print("----")
        time.sleep(0.2)
        
    GPIO.cleanup()