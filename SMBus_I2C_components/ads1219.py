"""
    ADS1219_Lib.py
Personal library for use with the ADS1219 Analog-to-Digital Converter
This library enables the creation of objects capable of reading voltages from the ADS1219's four inputs. 
The ADS1219 can also function as a comparator, but this library is focused on voltage reading capabilities.

This version is an initial release and is optimized for simplicity, focusing solely on voltage measurement functionality.

--Author     : ColinB27
--Revision   : 001
--First Rev. : 2024/02/28
--Last Rev.  : 2024/02/28
"""
# To accesss information or commands to each of these inputs use the 
# corresponding number of each inputs in function calls
# AIN0 - 0
# AIN1 - 1
# AIN2 - 2
# AIN3 - 3

from smbus2 import SMBus
from time import sleep

class Ads1219():
    def __init__(self,addr, i2c=2):
        self.addr = (addr)
        self.i2c = SMBus(i2c)
        self.ain_reg=((0x63, 0x83, 0xA3, 0xC3))
        self.ain_raw_data = [0,0,0,0] 
        self.ain_values   = [0,0,0,0] 
    
    def _read_ain_byte_data_(self, ain):
        self.i2c.write_byte_data(self.addr,0x40,self.ain_reg[ain]) # configures the adc to read a AN
        self.i2c.write_byte(self.addr,0x08) # calls a read action from the adc
        sleep(0.5)
        
        data = self.i2c.read_i2c_block_data(self.addr,0x10,3) # reads the value from the read action of the adc
        self.ain_raw_data[ain] = (((data[0] << 8)+ data[1])<< 8)+data[2]
        return data
    
    def _interpret_byte_data_(self,ain):
        if (self.ain_raw_data[ain] & 0x800000) == 0x800000: 
            volts = "Value is negative and out of range"
        else: 
            self.ain_values[ain] = round(((self.ain_raw_data[ain]*5)/2**23),4)
    
    def _read_ain_voltage_(self, ain):
        self._read_ain_byte_data_(ain)
        self._interpret_byte_data_(ain)
    
    def _read_adc_voltages_(self):
        for ain in range(0,4):
            self._read_ain_voltage_(ain)
            
