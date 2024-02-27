from smbus2 import SMBus

CLEAR = 0
RED   = 1
GREEN = 2
BLUE  = 3

# gains 0x0 0x1 0x2 0x3

class Adsp9960():
    def __init__(self, i2c=2):
        self.i2c = i2c
        self.addr = 0x39
        self.read_reg = (0x94,0x96,0x98,0x9A)
        self.color_data = [[],[],[],[]]
        
    def enable(self):
        self.i2c.write_byte_data(self.APDS9960_addr,0x80,0x01) # pwr on
        self.i2c.write_byte_data(self.APDS9960_addr,0x80,0x03) # enable
    
    def read_color(self, color):
        self.color_data[CLEAR] = self.read_ASL_register(CLEAR,2)
        self.color_data[RED]   = self.read_ASL_register(RED,2)
        self.color_data[GREEN] = self.read_ASL_register(GREEN,2)
        self.color_data[BLUE]  = self.read_ASL_register(BLUE,2)
        
    def set_gain(self, gain):
        if gain <=3 and gain >=0:
            self.i2c.write_byte_data(self.APDS9960_addr,0x8F,0x40)
    