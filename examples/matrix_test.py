from utime import sleep_ms, sleep
from colors import *
import pixelstrip

# This script tests whether the matrix options are set up properly.
# If set correctly, the origin pixel should be in the upper left 
# corner and BLUE/WHITE pixels should go left-to-right / top-to-bottom.

strip = pixelstrip.PixelStrip(4, width=8, height=8, options={pixelstrip.MATRIX_TOP, pixelstrip.MATRIX_LEFT})
TIME = 0.200

strip.clear()
while True:
    # Blink the zero pixel as RED
    for i in range(0, 6):
        strip[0] = RED
        strip.show()
        sleep(TIME)
        strip.clear()
        strip.show()
        sleep(TIME/2)
    sleep(0.500)

    # Blink the origin pixel as GREEN
    for i in range(0, 6):
        strip[0,0] = GREEN
        strip.show()
        sleep(TIME)
        strip.clear()
        strip.show()
        sleep(TIME/2)
    sleep(0.500)

    # Blink pixels in sequence as YELLOW
    for p in range(0, strip.n):
        strip[p] = YELLOW
        strip.show()
        sleep(TIME/2)
        strip.clear()
        strip.show()
        sleep(TIME/4)
    sleep(0.500)

    # Blink each row as BLUE or WHITE, top to bottom and left to right
    for y in range(0, strip.height):
        c = BLUE if y % 2 == 0 else WHITE
        for x in range(0, strip.width):
            strip[x,y] = c
            strip.show()
            sleep(TIME/2)
            strip.clear()
            strip.show()
            sleep(TIME/4)
    sleep(0.500)
