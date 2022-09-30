"""
Author: Jeremy Castagno
Description: Control Pico Explorer Board Speaker with Potentiometer
"""
import utime
import machine
from picographics import PicoGraphics, DISPLAY_PICO_EXPLORER
from pimoroni import Buzzer

# import our tone mapping
from tones import tone_list, max_freq

# setup the display
display = PicoGraphics(display=DISPLAY_PICO_EXPLORER)
# get width and height of display
WIDTH, HEIGHT = display.get_bounds()
# get background color pen (dark grey)
BG = display.create_pen(40, 40, 40)
# setup the potentiometer
potentiometer = machine.ADC(26)

# Create a buzzer on pin 0
# Don't forget to wire GP0 to AUDIO!
buzzer = Buzzer(0)

colors = [(0, 0, 255), (0, 255, 0), (255, 255, 0), (255, 0, 0)]

def percentage_to_color(percent):
    "Convert a number from 0 to 1 to an RGB color"
    f_index = (len(colors) - 1) * percent
    index = int(f_index)

    if index == len(colors) - 1:
        return colors[index]

    blend_b = f_index - index
    blend_a = 1.0 - blend_b

    a = colors[index]
    b = colors[index + 1]

    return [int((a[i] * blend_a) + (b[i] * blend_b)) for i in range(3)]

def play_tone(frequency):
    "This function will pay the tone (frequency) requested"
    buzzer.set_tone(frequency)

def draw_frequency(frequency):
    "This function will draw a colored bar based upon the frequency. Height and color changes"
    percent = frequency / max_freq
    color = percentage_to_color(percent)
    bar_width = WIDTH
    bar_height = int(percent * HEIGHT)
    bar_color = display.create_pen(*color)
    display.set_pen(bar_color)
    # x, y, width, height
    display.rectangle(0, HEIGHT-bar_height, bar_width, bar_height)

for i in range(0, max_freq):
    display.set_pen(BG)
    display.clear()

    value = potentiometer.read_u16()
    chosen_freq = int(max_freq * (value/ 65536))
    play_tone(chosen_freq)
    draw_frequency(chosen_freq)
    
    display.update()
    utime.sleep_ms(30)

