# -*- coding: utf-8 -*-
"""
Provides the Compass class, which can control the QMC5883L magnetometer
module.

"""

import math
import time

import smbus


#I2C Address
I2C_ADDRESS = 0x0D

#Register Addresses
CONTROL_REGISTER_1 = 0x09
CONTROL_REGISTER_2 = 0x0A
SET_RESET_PERIOD_REGISTER = 0x0B
DATA_REGISTER_BEGIN = 0x00
TEMP_REGISTER_BEGIN = 0x07


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
class MagnetometerData:
    
    def __init__(self):
        self.x_axis = 0
        self.y_axis = 0
        self.z_axis = 0


#Helper function
def signed_int(value):
    max_unsigned = 65536
    if value > (max_unsigned/2 - 1):
        return value-max_unsigned
    else:
        return value
        
    
#Gives the deafult config options
def get_default_config():
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
    def __init__(self, config=get_default_config()):
        self.bus = smbus.SMBus(1) #I2C channel = 1
        self.write(CONTROL_REGISTER_1, [config.OSR_RNG_ODR_MODE])
        self.write(CONTROL_REGISTER_2, [config.CR2_INT_ENABLE])
        self.write(SET_RESET_PERIOD_REGISTER, [config.SET_RESET_PERIOD])
        if config.OSR_RNG_ODR_MODE & 0b00010000 == 0b00010000:
            self.m_scale = 8 / 32768
        else:
            self.m_scale = 2 / 32768
    
    def get_heading(self):
        data = self.read_data()
        heading = math.atan2(data.y_axis, data.x_axis)
        declination_angle = math.radians(-0.22) #Found here: http://www.magnetic-declination.com/
        heading += declination_angle
        if heading < 0:
            heading += 2*math.pi
        if heading > 2*math.pi:
            heading -= 2*math.pi            
        return math.degrees(heading)
    
    def read_data(self):
        raw_data = self.read(DATA_REGISTER_BEGIN, 6)
        x_lsb = raw_data[0]
        x_msb = raw_data[1]
        y_lsb = raw_data[2]
        y_msb = raw_data[3]
        z_lsb = raw_data[4]
        z_msb = raw_data[5]

        #Python converts bits to unsigned integers, so the "signed_int"
        #function is used to convert these to signed integers
        data = MagnetometerData()     
        x_raw = signed_int(x_msb << 8 | x_lsb)
        y_raw = signed_int(y_msb << 8 | y_lsb)
        z_raw = signed_int(z_msb << 8 | z_lsb)   
        data.x_axis = x_raw*self.m_scale
        data.y_axis = y_raw*self.m_scale
        data.z_axis = z_raw*self.m_scale
        
        return data
            
    def write(self, address, data):
        self.bus.write_i2c_block_data(I2C_ADDRESS, address, data)
    
    def read(self, address, length):
        return self.bus.read_i2c_block_data(I2C_ADDRESS, address, length)
        
    
def test_compass():
    compass = Compass()
    end_time = time.time() + 8
    while time.time() < end_time:    
        print(compass.get_heading())    
        time.sleep(0.25)