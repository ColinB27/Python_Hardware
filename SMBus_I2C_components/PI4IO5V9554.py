from smbus2 import SMBus
from time import sleep

class Pi4IOE5V9535():
    def __init__(self, I2C, addr):
        self.I2c = I2C
        self.addr = addr
        self.input_port_register = 0x00 # memory reister of component`
        self.output_port_register = 0x03 # memory reister of component`
        self.port_config_register = 0x01 # memory reister of component
        self.output_port = 0x00
        self.port_config = 0x00 # config to be sent to the registers (define once setup is decided)
        
    
    # Sends the port direction configuration to a IO bank
    def send_dir(self):
        self.I2c.write_byte_data(self.addr, self.port_config_register, self.port_config)
    
    # Sends the port outputs' configuration of a IO bank
    def send_outs(self):
        self.I2c.write_byte_data(self.addr, self.output_port_register, self.output_port)
    
    # Changes and sends the port direction configuration to a IO bank
    def set_dir(self dir):
        self.port_config = dir
        self.send_dir()
    
    # Changes and sends the port outputs configuration to a IO bank
    def set_outs(self out):
        self.output_port = out
        self.send_outs

    # Returns read values of input at bank
    def Read(self,bank):
        data = self.I2c.read_i2c_block_data(self.addr, self.input_port_register,1)
        return data

    def toggle_io(self, bank, mask):
        self.set_outs(self.Read()^ mask)
