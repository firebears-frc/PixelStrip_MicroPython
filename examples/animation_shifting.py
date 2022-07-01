from utime import sleep
from math import sin, floor
from colors import *
import pixelstrip

PALETTE_SIZE=64
BRIGHTNESS = 0.20

class ShiftingAnimation(pixelstrip.Animation):
    """
    Create a smoothly varying depth across a strip of pixels.
    The color palette is then smoothly shifted over time, giving
    the impression of motion.
    See:  https://en.wikipedia.org/wiki/Color_cycling
    """
    def __init__(self):
        pixelstrip.Animation.__init__(self)
        self.color_set=[RED, ORANGE, YELLOW, BLACK]
        self._palette = []
        self._depth = []
        self.cycle_time = 2.0

    def reset(self, strip):
        strip.clear()
        self._palette = self.create_palette(self.color_set)
        self._depth = self.create_depth_map(strip.n)
        strip.show()

    def draw(self, strip, delta_time):
        t = pixelstrip.current_time() % self.cycle_time
        color_shift = floor(PALETTE_SIZE * t / self.cycle_time)
        for p in range(strip.n):
            d = floor(PALETTE_SIZE * self._depth[p])
            color = self._palette[(d + color_shift) % PALETTE_SIZE]
            strip[p] = color
        strip.show()
    
    def create_depth_map(self, size):
        """
        Create an array the same length as a PixelStrip.  Each element 
        in the array is a floating point number between 0.0 and 1.0.
        This implementation just creates a sin curve.
        """
        depth = []
        for p in range(size):
            theta = (2.0 * p / size) * 3.14159
            depth.append(abs(sin(theta)))
        return depth

    def create_palette(self, color_set):
        """
        Create a list of color tuples, where the colors blend
        smoothly into each other.
        """
        palette = []
        for i in range(PALETTE_SIZE):
            palette.append(BLACK)
        m = PALETTE_SIZE / len(color_set)
        for i in range(PALETTE_SIZE):
            j = int(i / m)
            color1 = color_set[j]
            color2 = color_set[(j+1)%len(color_set)]
            n = int(i % m)
            palette[i] = self.average_color(color1, color2, n, m)
        return palette
    
    def average_color(self, color1, color2, n, m):
        r = int(color2[0]*n/m + color1[0]*(m-n)/m)
        g = int(color2[1]*n/m + color1[1]*(m-n)/m)
        b = int(color2[2]*n/m + color1[2]*(m-n)/m)
        return (r, g, b)


class ShiftingMatrixAnimation(ShiftingAnimation):
    """
    Create a smoothly varying depth across a matrix of pixels.
    """
    def __init__(self):
        ShiftingAnimation.__init__(self)

    def create_depth_map(self, size):
        """
        Create an array the same length as a PixelStrip.  Each element 
        in the array is a floating point number between 0.0 and 1.0.
        This implementation just creates a sin curve.
        """
        depth = []
        for p in range(size):
            theta = (2.0 * p / size) * 3.14159
            depth.append(abs(sin(theta)))
        return depth

# def main():
#     strip = pixelstrip.PixelStrip(4, 64, brightness=BRIGHTNESS)
#     strip.animation = ShiftingAnimation()
#     while True:
#         strip.draw()
#
# main()
