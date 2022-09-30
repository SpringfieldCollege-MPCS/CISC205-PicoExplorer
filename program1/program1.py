from machine import Pin
import time

led = Pin(0, Pin.OUT)

for i in range(10):
    led.toggle()
    time.sleep(1)