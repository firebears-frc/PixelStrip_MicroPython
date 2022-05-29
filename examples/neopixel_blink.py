from utime import sleep
from npxl import NeoPixel
from colors import *

strip = NeoPixel(4, 8)
strip.fill(BLACK)

while True:
    strip[0] = YELLOW
    strip.show()
    sleep(1.0)
    strip.fill(BLACK)
    strip.show()
    sleep(1.0)
    
