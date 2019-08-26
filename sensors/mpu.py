# -*- coding: utf-8 -*-

import math
import time

import smbus

from utils.updater import Updater


# Register
_POWER_MANAGEMENT_1 = 0x6b
_POWER_MANAGEMENT_2 = 0x6c
 
_I2C_ADDRESS = 0x68       # via i2cdetect

# Calibration Constants
_MPU_GZ_OFFSET = 1.75
_MPU_GZ_MIN = 0.35

def _signed_int(value):
    max_unsigned = 65536
    if value > (max_unsigned/2 - 1):
        return value-max_unsigned
    else:
        return value
    
    
class _MpuData:
    
    def __init__(self):
        self.ax = 0
        self.ay = 0
        self.az = 0
        self.gx = 0
        self.gy = 0
        self.gz = 0
    
class Mpu:
    
    def __init__(self):
        self._bus = smbus.SMBus(1)
        self._write(_POWER_MANAGEMENT_1, [0])
        self.roll = 0
        self.tilt = 0
        self.yaw = 0
        
    def update(self, dt):
        data = self._get_mpu_data()
        self.roll = math.degrees(math.atan2(data.az, data.ay))
        self.tilt = math.degrees(math.atan2(data.az, data.ax))
        delta_yaw = data.gz - _MPU_GZ_OFFSET
        if abs(delta_yaw) < _MPU_GZ_MIN:
            delta_yaw = 0
        self.yaw += delta_yaw * dt
        if self.yaw <= -180:
            self.yaw += 360
        elif self.yaw >= 180:
            self.yaw -= 360
        
    def _get_mpu_data(self):
        data = self._read(0x3B, 6)
        ax_msb = data[0]
        ax_lsb = data[1]
        ay_msb = data[2]
        ay_lsb = data[3]
        az_msb = data[4]
        az_lsb = data[5]
        ax = _signed_int(ax_msb << 8 | ax_lsb)
        ay = _signed_int(ay_msb << 8 | ay_lsb)
        az = _signed_int(az_msb << 8 | az_lsb)
        ax_scaled = ax / 16384
        ay_scaled = ay / 16384
        az_scaled = az / 16384
        
        data = self._read(0x43, 6)
        gx_msb = data[0]
        gx_lsb = data[1]
        gy_msb = data[2]
        gy_lsb = data[3]
        gz_msb = data[4]
        gz_lsb = data[5]
        gx = _signed_int(gx_msb << 8 | gx_lsb)
        gy = _signed_int(gy_msb << 8 | gy_lsb)
        gz = _signed_int(gz_msb << 8 | gz_lsb)
        gx_scaled = gx / 131
        gy_scaled = gy / 131
        gz_scaled = gz / 131
        
        data = _MpuData()
        data.ax = ax_scaled
        data.ay = ay_scaled
        data.az = az_scaled
        data.gx = gx_scaled
        data.gy = gy_scaled
        data.gz = gz_scaled
        
        return data
     
    def _write(self, address, data):
        self._bus.write_i2c_block_data(_I2C_ADDRESS, address, data)
    
    def _read(self, address, length):
        return self._bus.read_i2c_block_data(_I2C_ADDRESS, address, length)
    
    
def test_mpu():
    mpu = Mpu()
    updater = Updater(0.01)
    updater.add(mpu.update)
    print_yaw = lambda dt: print("Heading: {}".format(mpu.yaw))
    updater.add(print_yaw, 0.5)
    
    while updater.timer <= 60:
        updater.update()    