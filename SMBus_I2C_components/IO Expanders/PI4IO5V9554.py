"""
============================================================================================
Python Library for PI4IO5V9554 8-bit I/O Expander
Description:
This library provides a class and functions to interact with the PI4IO5V9554 I/O expander.
Please note that this library is designed to be used with Python 3.5.7 and newer versions.

Author: ColinB27
Revision: 2
First Revision: 02/27/2024
Latest Revision: 08/18/2025 
============================================================================================
"""

from smbus2 import SMBus
from time import sleep

INPUT_PORT_REGISTER  = 0x00 # memory reister of component` make definitions to avoid creating this data each iterations
PORT_CONFIG_REGISTER = 0x01 # memory reister of component //
OUTPUT_PORT_REGISTER = 0x03 # memory reister of component` //

class Pi4IOE5V9535():
    def __init__(self, I2C, addr, config =0x00, outputs=0x00):
        self.I2c = I2C
        self.addr = addr

        self.output_port = outputs # outputs to be sent to the registers 
        self.port_config = config  # config to be sent to the registers 
        
    # Sends the port direction configuration to a IO bank
    def send_dir(self):
        self.I2c.write_byte_data(self.addr, PORT_CONFIG_REGISTER, self.port_config)
    
    # Sends the port outputs' configuration of a IO bank
    def send_outs(self):
        self.I2c.write_byte_data(self.addr, OUTPUT_PORT_REGISTER, self.output_port)
    
    # Changes and sends the port direction configuration to a IO bank
    def set_dir(self, dir):
        self.port_config = dir
        self.send_dir()
    
    # Changes and sends the port outputs configuration to a IO bank
    def set_outs(self, out):
        self.output_port = out
        self.send_outs

    # Returns read values of input at bank
    def Read(self):
        data = self.I2c.read_i2c_block_data(self.addr, INPUT_PORT_REGISTER,1)
        return data

    def toggle_io(self, mask):
        self.set_outs(self.Read()^ mask)
