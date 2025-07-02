from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_io16_v2 import BrickletIO16V2

class io_16_setup(BrickletIO16V2):
    def __init__(self, UID:str, IPCON:IPConnection):
        super().__init__(UID, IPCON);
        self.status = 0 #follow biary tracking on 16 bits for status

    def get_value(self): #reads values and returns a int that each bit represents the state of all relays : -> 0b1100 means that relays 3 and 4 are active
        return int(''.join(str(i) for i in list(map(int,(super().get_value())))), 2)

    def set_value(self,value): #reads values using an int where each bit represents the state of all relays : 0b1111 -> will activte relays 0 through 3
        return super().set_value([bit=='1' for bit in ((bin(value)))[2::].zfill(16)[::-1]])

    def reset_outputs(self):
        self.set_value(0)
        
    def update_status(self):
        self.status = self.get_value()

    def configure_all_out(self):
        for IO in range(0,16): self.set_configuration(IO,"o",False)
