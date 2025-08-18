"""
============================================================================================
Python Library for PI4IOE5V9535 8-bit I/O Expander
Description:
This library provides a class and functions to interact with the PI4IOE5V9535 I/O expander.
Please note that this library is designed to be used with Python 3.5.7 and newer versions.

Author: ColinB27
Revision: 2
First Revision: 02/27/2024
Latest Revision: 08/18/2025 
============================================================================================
"""

INPUT_PORT_REGISTERS  = (0x00,0x01) # memory reister of component
OUTPUT_PORT_REGISTERS = (0x02,0x03) # memory reister of component
CONFIG_PORT_REGISTERS = (0x06,0x07) # memory reister of component
        
class PI4IOE5V9535():
    def __init__(self, I2C, addr, config = [0x00,0x00], outputs = [0x00, 0x00]):
        self.I2c = I2C
        self.addr = addr

        self.port_config  = config  # config to be sent to the registers 
        self.output_ports = outputs # outputs to be sent to the registers
    
    # Sends the port direction configuration to a IO bank
    def send_dir(self, bank):
        self.I2c.write_byte_data(self.addr, CONFIG_PORT_REGISTERS[bank], self.port_config[bank])
    
    # Sends the port outputs' configuration of a IO bank
    def send_outs(self, bank):
        self.I2c.write_byte_data(self.addr, OUTPUT_PORT_REGISTERS[bank], self.output_ports[bank])
    
    # Changes and sends the port direction configuration to a IO bank
    def set_dir(self, bank, dir):
        self.port_config[bank] = dir
        self.send_dir(bank)
    
    # Changes and sends the port outputs configuration to a IO bank
    def set_outs(self, bank, out):
        self.output_ports[bank] = out
        self.send_outs(bank)

    # Returns read values of input at bank
    def Read(self,bank):
        data = self.I2c.read_i2c_block_data(self.addr, INPUT_PORT_REGISTERS[bank],1)
        return data

    def toggle_io(self, bank, mask):
        self.set_outs(bank,self.Read(bank)[0]^ mask)
