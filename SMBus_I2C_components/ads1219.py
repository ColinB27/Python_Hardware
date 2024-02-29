from smbus2 import SMBus
from time import sleep

# To accesss information or commands to each of these inputs use the 
# corresponding number of each inputs in function calls
# AIN0 - 0
# AIN1 - 1
# AIN2 - 2
# AIN3 - 3

class Ads1219():
    def __init__(self,addr, i2c=2):
        self.addr = addr
        self.i2c = SMBus(i2c)
        self.ain_reg=((0x63, 0x83, 0xA3, 0xC3))
        self.ain_values = [0,0,0,0] 
    
    def _read_ain_byte_data_(self, ain):
        self.i2c.write_byte_data(self.addr,0x40,self.ain_reg[ain]) # configures the adc to read a AN
        self.i2c.write_byte(self.addr,0x08) # calls a read action from the adc
        sleep(0.5)
        
        data = self.i2c.read_i2c_block_data(self.addr,0x10,3) # reads the value from the read action of the adc
        self.ain_values[ain] = (((data[0] << 8)+ data[1])<< 8)+data[2]
    
    def _interpret_byte_data_(self,ain):
        if (self.ain_values[ain] & 0x800000) == 0x800000: 
            volts = "Value is negative and out of range"
        else: 
            self.ain_values[ain] = round(((self.ain_values[ain]*5)/2**23),4)
    
    def _read_ain_voltage_(self, ain):
        self._read_ain_byte_data_(ain)
        self._interpret_byte_data_(ain)
    
    def _read_adc_voltages_(self):
        for ain in range(0,4):
            self._read_ain_voltage_(ain)
            
