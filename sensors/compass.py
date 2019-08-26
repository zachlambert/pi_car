# -*- coding: utf-8 -*-
"""
Provides the Compass class, which can control the QMC5883L magnetometer
module.

"""

import math
import time

import matplotlib.pyplot as plt
import numpy as np
import smbus


#I2C Address
_I2C_ADDRESS = 0x0D

#Register Addresses
_CONTROL_REGISTER_1 = 0x09
_CONTROL_REGISTER_2 = 0x0A
_SET_RESET_PERIOD_REGISTER = 0x0B
_DATA_REGISTER_BEGIN = 0x00
_TEMP_REGISTER_BEGIN = 0x07

#Compass Calibration Values
_MAGNETOMETER_X_OFFSET = 0.00244
_MAGNETOMETER_Y_OFFSET = -0.0843

#Class for storing configuration options
class CompassConfig:
    
    def __init__(self):
        self.OVL_DRDY = 0
        self.TOUT_LSB = 0
        self.TOUT_MSB = 0
        self.OSR_RNG_ODR_MODE = 0
        self.CR2_INT_ENABLE = 0
        self.SET_RESET_PERIOD = 0
        

#Class for storing the magnetic field strength in each axis
class _MagnetometerData:
    
    def __init__(self):
        self.x_axis = 0
        self.y_axis = 0
        self.z_axis = 0


#Helper function
def _signed_int(value):
    max_unsigned = 65536
    if value > (max_unsigned/2 - 1):
        return value-max_unsigned
    else:
        return value
        
    
#Gives the deafult config options
def _get_default_config():
    OSR = 0b00
    RNG = 0b00
    ODR = 0b00
    MODE = 0b01
    CR2 = 0b00000000
    RESET_PERIOD = 0b00000001
    
    config = CompassConfig()
    config.OSR_RNG_ODR_MODE |= OSR << 6
    config.OSR_RNG_ODR_MODE |= RNG << 4
    config.OSR_RNG_ODR_MODE |= ODR << 2
    config.OSR_RNG_ODR_MODE |= MODE    
    config.CRC_INT_ENABLE = CR2
    config.SET_RESET_PERIOD = RESET_PERIOD
    
    return config
        

#Compass class. Configures the QMC5883L module, reads data from it, and processes
#this to give the heading.
class Compass:
    
    #Can load with a specific config, or if left blank, loads the default config
    def __init__(self, config=_get_default_config()):
        self._bus = smbus.SMBus(1) #I2C channel = 1
        self._write(_CONTROL_REGISTER_1, [config.OSR_RNG_ODR_MODE])
        self._write(_CONTROL_REGISTER_2, [config.CR2_INT_ENABLE])
        self._write(_SET_RESET_PERIOD_REGISTER, [config.SET_RESET_PERIOD])
        if config.OSR_RNG_ODR_MODE & 0b00010000 == 0b00010000:
            self._scale = 8 / 32768
        else:
            self._scale = 2 / 32768
    
    def get_heading(self):
        data = self._read_data()
        heading = math.degrees(math.atan2(
            (data.y_axis - _MAGNETOMETER_Y_OFFSET),
            (data.x_axis - _MAGNETOMETER_X_OFFSET)))
        declination_angle = -0.22 #Found here: http://www.magnetic-declination.com/
        heading += declination_angle
        if heading < 0:
            heading += 360
        if heading > 360:
            heading -= 360            
        return heading
    
    def calibrate(self, update_func=None, TIME_STEP=0.05):
        finished = False
        plots = []
        while not finished:
            SAMPLE_TIME = 6
            NUM_SAMPLES = int(SAMPLE_TIME / TIME_STEP)
            data = None
            points = np.zeros((NUM_SAMPLES,2))
            for i in range(points.shape[0]):
                data = self._read_data()
                points[i] = (data.x_axis, data.y_axis)
                if update_func != None:
                    update_func()
                time.sleep(TIME_STEP)
            min_x = np.min(points[:, 0])
            max_x = np.max(points[:, 0])
            min_y = np.min(points[:, 1])
            max_y = np.max(points[:, 1])
            x_centre = (min_x + max_x) / 2
            y_centre = (min_y + max_y) / 2
            print("Calibration factors:")
            print("X:{}, Y:{}".format(x_centre, y_centre))
            
            plots.append(points)
            
            plt.figure()
            ax = plt.gca()
            for stored_points in plots:
                ax.plot(stored_points[:, 0], stored_points[:, 1])
            ax.spines['left'].set_position('zero')
            ax.spines['right'].set_color('none')
            ax.spines['bottom'].set_position('zero')
            ax.spines['top'].set_color('none')
            plt.savefig('calibration.png')
            
            print("Finished. Type anything to repeat.")
            user_input = input(">")
            if user_input=="":
                finished = True
                
    def _read_data(self):
        raw_data = self._read(_DATA_REGISTER_BEGIN, 6)
        x_lsb = raw_data[0]
        x_msb = raw_data[1]
        y_lsb = raw_data[2]
        y_msb = raw_data[3]
        z_lsb = raw_data[4]
        z_msb = raw_data[5]

        #Python converts bits to unsigned integers, so the "signed_int"
        #function is used to convert these to signed integers
        x_raw = _signed_int(x_msb << 8 | x_lsb)
        y_raw = _signed_int(y_msb << 8 | y_lsb)
        z_raw = _signed_int(z_msb << 8 | z_lsb)   
        data = _MagnetometerData()     
        data.x_axis = x_raw*self._scale
        data.y_axis = y_raw*self._scale
        data.z_axis = z_raw*self._scale
        
        return data
            
    def _write(self, address, data):
        self._bus.write_i2c_block_data(_I2C_ADDRESS, address, data)
    
    def _read(self, address, length):
        return self._bus.read_i2c_block_data(_I2C_ADDRESS, address, length)
        
    
def test_compass():
    compass = Compass()
    compass.calibrate()
    end_time = time.time() + 10
    while time.time() < end_time:    
        print(compass.get_heading())
        time.sleep(0.25)
        