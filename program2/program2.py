from machine import Pin
import utime
from picographics import PicoGraphics, DISPLAY_PICO_EXPLORER

# Create an output pin object for our LED
led = Pin(0, Pin.OUT)
# Create an input pin object for our switch
# DONT FORGET the Pin.PULL_UP to add a pull up resistor in the circuit 
button = Pin(1, Pin.IN, Pin.PULL_UP)
# setup the display
display = PicoGraphics(display=DISPLAY_PICO_EXPLORER)
# get width and height of display
WIDTH, HEIGHT = display.get_bounds()
# get background color pen (dark grey)
BG = display.create_pen(40, 40, 40)
RECT_COLOR = display.create_pen(255, 255, 0)
rect_size = 80

while True:
    # clear the display to background color
    display.set_pen(BG)
    display.clear()

    # if the button is NOT pressed, it defaults to high voltage
    # this is a 1 (true) returned by button.value()
    # therefore we need to invert the value to get the 
    # switch_on flag to be correct
    switch_on = not button.value()
    if switch_on:
        led.value(1)
        # update the display
        display.set_pen(RECT_COLOR)
        display.rectangle(120, 120, rect_size, rect_size)  # x, y, width, height
    else:
        led.value(0)
    display.update()
    utime.sleep_ms(30)