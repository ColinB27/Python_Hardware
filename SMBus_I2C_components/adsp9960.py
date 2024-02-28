"""
============================================================================================
Python Library for APDS9960 Light and Gesture Sensor
Author: ColinB27
Revision : 1
First revision  : 02/27/2024
Latest revision : 02/27/2024 

Description:
This library provides a class and functions to interact with the APDS9960 light sensor.
The library currently only supports functionalities related to the light sensor. 
The gesture sensor functionality is not implemented in this version of the library.
Please note that this library is designed to be used with Python 3.5.7 and newer versions

============================================================================================
"""
from smbus2 import SMBus

CLEAR = (0)
RED   = (1)
GREEN = (2)
BLUE  = (3)
APDS9960_EN_REG = (0x80)
APDS9960_GAIN_REG = (0x8F)

# gains 0x0 0x1 0x2 0x3

class Adsp9960():
    def __init__(self, i2c=2):
        self.i2c = SMBus(i2c)
        self.addr = (0x39)
        self.read_reg = (0x94,0x96,0x98,0x9A)
        self.color_data = [[],[],[],[]]
        
    def enable_color(self):
        self.i2c.write_byte_data(self.APDS9960_addr,APDS9960_EN_REG,0x01) # pwr on
        self.i2c.write_byte_data(self.APDS9960_addr,APDS9960_EN_REG,0x03) # enable

    def read_ambient_light_register(self, color):
        if color <= 0 and color >=3:
            data = self.i2c.read_i2c_block_data(self.APDS9960_addr,self.read_reg[color],2)
            self.color_data[color] = data
            return data
        else:
            return -1
    
    def read_colors(self):
        self.color_data[CLEAR] = self.read_ambient_light_register(CLEAR)
        self.color_data[RED]   = self.read_ambient_light_register(RED)
        self.color_data[GREEN] = self.read_ambient_light_register(GREEN)
        self.color_data[BLUE]  = self.read_ambient_light_register(BLUE)
        return self.color_data
        
    def set_gain(self, gain):
        if gain <=3 and gain >=0:
            self.i2c.write_byte_data(self.APDS9960_addr,APDS9960_GAIN_REG,gain)
            
    def get_stored_color_data(self,color):
        if color <=3 and color >=0:
            return self.color_data[color]
        else:
            return -1
    
