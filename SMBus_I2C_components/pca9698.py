"""
============================================================================================
Python Library for PCA9698 40-bit I/O Expander
Description:
This library provides a class and functions to interact with the PCA9698 I/O expander.
Please note that this library is designed to be used with Python 3.5.7 and newer versions.

Author: ColinB27
Revision: 1
First Revision: 02/27/2024
Latest Revision: 02/27/2024 
============================================================================================
"""

from smbus2 import SMBus
from time import sleep

class IoExp():
    def __init__(self,addr = 0x20, i2c=2, port_dir = [0x00,0x00,0x00,0x00,0x00], port_out = [0x00,0x00,0x00,0x00,0x00]):
        self.addr = addr
        self.bus = SMBus(i2c)
        self.port_reg      = (0x00,0x01,0x02,0x03,0x04) # memory register of IO values
        self.output_reg    = (0x08,0x09,0x0A,0x0B,0x0C) # memory register of IO outputs
        self.direction_reg = (0x18,0x19,0x1A,0x1B,0x1C) # memory register of IO direction (in or out) (1 is and input 0 is an output)
        
        self.port_dir = port_dir # config to send to the direction register
        self.port_out = port_out # config to send to the output register
    
    # Sends the port direction configuration to a IO bank
    def _IOExp_send_dir_(self, bank):
        self.bus.write_byte_data(self.addr, self.direction_reg[bank], self.port_dir[bank])
        sleep(0.2)
    
    # Sends the port outputs' configuration of a IO bank
    def _IOExp_send_outs_(self, bank):
        self.bus.write_byte_data(self.addr, self.output_reg[bank], self.port_out[bank])
        sleep(0.2)
    
    # Changes and sends the port direction configuration to a IO bank
    def _IOExp_set_dir_(self, bank, dir):
        self.port_dir[bank] = dir
        self._IOExp_send_dir_(bank)
    
    # Changes and sends the port outputs configuration to a IO bank
    def _IOExp_set_outs_(self, bank, out):
        self.port_out[bank] = out
        self._IOExp_send_outs_(bank)

    # Returns read values of input at bank
    def _IOExp_read_(self,bank):
        data = self.bus.read_i2c_block_data(self.addr, self.port_reg[bank],1)
        return data
    
    # Configures the OI expander using the configuration set in the registers
    def _IOExp_configure_(self):
        for x in range(0,5):
            self._IOExp_send_dir_(x)
            self._IOExp_send_outs_(x)
    
    def _toggle_io_(self, bank, io):
        bit = 1
        for i in range(0,io):
            bit = bit << 1
        if io >= 0 and io <=7 and self.port_dir[io]:
            if(self.port_out[io] & bit):
                integer = integer - bit
            else:
                integer = integer + bit
            return integer
        else:
            return -1;
