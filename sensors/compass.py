"""
compass.py

Purpose: Provide the Compass class, which can control the QMC5883L magnetometer
module.

"""

import smbus
import time
import math

#I2C Address
QMC5883L_Address = 0x0D

#Register Addresses
ControlRegister1 = 0x09
ControlRegister2 = 0x0A
SetResetPeriodRegister = 0x0B
DataRegisterBegin = 0x00
TempRegisterBegin = 0x07

#Class for storing configuration options
class QMC5883L_Config:
    
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
        self.XAxis = 0
        self.YAxis = 0
        self.ZAxis = 0

#Helper function
def signedInt(value):
    max_unsigned = 65536
    
    if value > (max_unsigned/2 - 1):
        return value - max_unsigned
    else:
        return value
        
#Gives the deafult config options
def getDefaultConfig():
    
    OSR = 0b00
    RNG = 0b00
    ODR = 0b00
    MODE = 0b01
    CR2 = 0b00000000
    RESETPERIOD = 0b00000001
    
    config = QMC5883L_Config()
    config.OSR_RNG_ODR_MODE |= OSR << 6
    config.OSR_RNG_ODR_MODE |= RNG << 4
    config.OSR_RNG_ODR_MODE |= ODR << 2
    config.OSR_RNG_ODR_MODE |= MODE    
    config.CRC_INT_ENABLE = CR2
    config.SET_RESET_PERIOD = RESETPERIOD
    
    return config
        

#Compass class. Configures the QMC5883L module, reads data from it, and processes
#this to give the heading.
        
class QMC5883L:
    
    #Can load with a specific config, or if left blank, loads the default config
    def __init__(self, config=getDefaultConfig()):
        
        self.m_scale = 0.0
        self.bus = smbus.SMBus(1) #I2C channel = 1
            
        self.Write(ControlRegister1, [config.OSR_RNG_ODR_MODE])
        self.Write(ControlRegister2, [config.CR2_INT_ENABLE])
        self.Write(SetResetPeriodRegister, [config.SET_RESET_PERIOD])
        
        if config.OSR_RNG_ODR_MODE & 0b00010000 == 0b00010000:
            self.m_Scale = 8 / 32768
        else:
            self.m_Scale = 2 / 32768
    
    def getHeading(self):
        
        data = self.ReadData()
        
        heading = math.atan2(data.YAxis, data.XAxis)
        
        #Found declination angle here: http://www.magnetic-declination.com/
        declinationAngle = math.radians(-0.22)
        heading += declinationAngle
        
        if heading < 0:
            heading += 2*math.pi
        if heading > 2*math.pi:
            heading -= 2*math.pi
            
        return math.degrees(heading)
    
    def ReadData(self):

        raw_data = self.Read(DataRegisterBegin, 6)
        
        X_LSB = raw_data[0]
        X_MSB = raw_data[1]
        Y_LSB = raw_data[2]
        Y_MSB = raw_data[3]
        Z_LSB = raw_data[4]
        Z_MSB = raw_data[5]

        #Python converts them to unsigned integers, so need to
        #convert to signed                
        x_raw = signedInt(X_MSB << 8 | X_LSB)
        y_raw = signedInt(Y_MSB << 8 | Y_LSB)
        z_raw = signedInt(Z_MSB << 8 | Z_LSB)
        
        #Put data in a MagnetometerData object
        data = MagnetometerData()        
        data.XAxis = x_raw * self.m_Scale
        data.YAxis = y_raw * self.m_Scale
        data.ZAxis = z_raw * self.m_Scale
        
        return data
            
        
    def Write(self, address, data):
        self.bus.write_i2c_block_data(QMC5883L_Address, address, data)
    
    def Read(self, address, length):
        return self.bus.read_i2c_block_data(QMC5883L_Address, address, length)
        
    
def testCompass():
    
    compass = QMC5883L()

    #Start loop
    
    end_time = time.time() + 8
    
    while time.time() < end_time:
        
        print(compass.getHeading())
        
        time.sleep(0.25)