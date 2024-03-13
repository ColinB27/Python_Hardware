# Components

## ADS1219 Analog to digital converter and comparator 4 inputs
### Basic Use 
```python
from smbus2 import SMBus
from ads1219 import Ads1219

addr = 0x40
adc = Ads1219(addr)
```

## ADSP9960 Light and gesture sensor
### Basic Use
```python
from smbus2 import SMBus
from adsp9960 import Adsp9960

light_sensonr = Adsp9960()
light_sensor.enable_color()
light_sensor.set_gain(0x03)
ambient_red_light = light_sensor.read_ambient_light_register(RED, 2)
all_light = light_sensor.read_colors()
```

## PCA9698 40 bit IO expander
