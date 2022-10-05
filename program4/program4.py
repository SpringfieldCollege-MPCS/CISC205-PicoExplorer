import utime

from pimoroni_i2c import PimoroniI2C
from breakout_dotmatrix import BreakoutDotMatrix
from pimoroni import PICO_EXPLORER_I2C_PINS
from pimoroni import Button

# configure the dot matrix
i2c = PimoroniI2C(**PICO_EXPLORER_I2C_PINS)
display = BreakoutDotMatrix(i2c, address=0x61)
display.clear()
display.show()

# configure the A and X button for input
button_a = Button(12, repeat_time=1000, hold_time=500)
button_x = Button(14, repeat_time=1000, hold_time=500)

count = 0
while True:
    # read buttons and increment count
    if button_a.read():
        count += 1
        count = min(99, count)
    if button_x.read():
        count -= 1
        count = max(0, count)

    # convert count to a string
    count_str = str(count)
    left_num = '0' if count < 10 else count_str[0]
    right_num = count_str[0] if count < 10 else count_str[1]
    
    # display count on LED matrix
    display.set_character(0, ord(left_num))
    display.set_character(5, ord(right_num))
    display.show()

    utime.sleep_ms(30)

