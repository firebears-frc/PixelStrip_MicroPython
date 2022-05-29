from utime import sleep
from colors import *
import pixelstrip

class SpinningAnimation(pixelstrip.Animation):
    """
    One colored pixel travels across the strip.
    """
    def __init__(self, color, cycle_time=1.0, name=None):
        pixelstrip.Animation.__init__(self, name)
        self.color = color
        self.current_pixel = 0
        self.cycle_time = cycle_time
        self.wait_time = self.cycle_time / 8

    def reset(self, strip):
        self.current_pixel = 0
        self.wait_time = self.cycle_time / strip.n
        self.timeout = self.wait_time

    def draw(self, strip, delta_time):
        if self.is_timed_out():
            self.timeout = self.wait_time
            self.current_pixel = (self.current_pixel + 1) % strip.n
            strip.clear()
            strip[self.current_pixel] = self.color
            strip.show()


# def main():
#     strip = pixelstrip.PixelStrip(4, 8)
#     strip.animation = SpinningAnimation(LIGHTBLUE)
#     while True:
#         strip.draw()
#         sleep(0.02)

# main()


