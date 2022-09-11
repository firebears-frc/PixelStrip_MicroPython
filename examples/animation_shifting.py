from utime import sleep
from math import sin, floor
from random import random
from colors import *
import pixelstrip

PALETTE_SIZE = 64
BRIGHTNESS = 0.20


class ShiftingAnimation(pixelstrip.Animation):
    """
    Create a smoothly varying depth across a strip of pixels.
    The color palette is then smoothly shifted over time, giving
    the impression of motion.
    See:  https://en.wikipedia.org/wiki/Color_cycling
    """

    def __init__(self, stride=8):
        pixelstrip.Animation.__init__(self)
        self.color_set = [BLUE, YELLOW]
        self._palette = []
        self._depth = []
        self.cycle_time = 2.0
        self.stride = stride

    def reset(self, strip):
        strip.clear()
        self._palette = self.create_palette(self.color_set)
        self._depth = self.create_depth_map(strip)
        strip.show()

    def draw(self, strip, delta_time):
        t = pixelstrip.current_time() % self.cycle_time
        color_shift = floor(PALETTE_SIZE * t / self.cycle_time)
        for p in range(strip.n):
            d = floor(PALETTE_SIZE * self._depth[p])
            color = self._palette[(d + color_shift) % PALETTE_SIZE]
            strip[p] = color
        strip.show()

    def create_depth_map(self, strip):
        """
        Create an array the same length as a PixelStrip.  Each element 
        in the array is a floating point number between 0.0 and 1.0.
        This implementation just creates a sin curve.
        """
        depth = []
        for p in range(strip.n):
            theta = (2.0 * p / strip.n) * 3.14159
            f = abs(sin(theta))
            depth.append(f)
        return depth

    def create_palette(self, color_set):
        """
        Create a list of color tuples, where the colors blend
        smoothly into each other.
        """
        palette = []
        for _ in range(PALETTE_SIZE):
            palette.append(BLACK)
        m = PALETTE_SIZE / len(color_set)
        for i in range(PALETTE_SIZE):
            j = int(i / m)
            color1 = color_set[j]
            color2 = color_set[(j+1) % len(color_set)]
            n = int(i % m)
            palette[i] = self.average_color(color1, color2, n, m)
        return palette

    def average_color(self, color1, color2, n, m):
        r = int(color2[0]*n/m + color1[0]*(m-n)/m)
        g = int(color2[1]*n/m + color1[1]*(m-n)/m)
        b = int(color2[2]*n/m + color1[2]*(m-n)/m)
        return (r, g, b)


class Matrix:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.shape = (width, height)
        self.val = []
        for _ in range(self.width * self.height):
            self.val.append(0.0)

    def __setitem__(self, index, value):
        nn = index[0] + index[1]*self.width if type(index) is tuple else index
        self.val[nn] = value

    def __getitem__(self, index):
        nn = index[0] + index[1]*self.width if type(index) is tuple else index
        return self.val[nn]

    def min(self):
        mn = self.val[0]
        for v in self.val:
            mn = min(mn, v)
        return mn

    def max(self):
        mx = self.val[0]
        for v in self.val:
            mx = max(mx, v)
        return mx

    def valid(self, index):
        return index[0] >= 0 and index[0] < self.width and index[1] >= 0 and index[1] < self.height

    def average(self, *args):
        count = 0
        sum = 0.0
        for index in args:
            if self.valid(index):
                count += 1
                sum += self[index]
        return sum / count if count > 0 else 0.0

    def square_average(self, index, n):
        return self.average((index[0], index[1]),
                            (index[0]+n, index[1]),
                            (index[0], index[1]+n),
                            (index[0]+n, index[1]+n))

    def diamond_average(self, index, n):
        return self.average((index[0], index[1]),
                            (index[0]+n, index[1]-n),
                            (index[0]+n*2, index[1]),
                            (index[0]+n, index[1]+n))

    def depth_map(self):
        mn = self.min()
        mx = self.max()
        d = []
        for v in self.val:
            value = (v - mn) / (mx - mn) if mx > mn else 0.0
            d.append(value)
        return d


class ShiftingMatrixAnimation(ShiftingAnimation):
    """
    Create a smoothly varying depth across a matrix of pixels.
    """

    def __init__(self, stride=8):
        ShiftingAnimation.__init__(self, stride)

    def _rand(self, s=8):
        return random() * s / self.stride

    def create_depth_map(self, strip):
        """
        Create an array the same size and shape as a PixelStrip matrix.  
        Each array element is a floating point number between 0.0 and 1.0.
        See:  https://en.wikipedia.org/wiki/Diamond-square_algorithm
        """
        m = Matrix(width=strip.width, height=strip.height)
        s = self.stride

        # Initialize corner values
        for yy in range(0, m.height, s):
            for xx in range(0, m.width, s):
                m[xx, yy] = self._rand(s=s)

        # Initial diamond step
        for yy in range(0, m.height, s):
            for xx in range(0, m.width, s):
                s2 = floor(s/2)
                m[xx+s2, yy +
                    s2] = m.diamond_average((xx, yy), s2) + self._rand(s=s2)

        # Loop until everything is filled
        while s > 1:
            s2 = floor(s/2)
            # Perform square step
            for yy in range(0, m.height, s):
                for xx in range(0, m.width, s):
                    m[xx+s2,
                        yy] = m.square_average((xx, yy), s2) + self._rand(s=s2)

            # Perform diamond step
            for yy in range(0, m.height, s):
                for xx in range(0, m.width, s):
                    m[xx+s2, yy +
                        s2] = m.diamond_average((xx, yy), s2) + self._rand(s=s2)

            s = floor(s/2)

        return m.depth_map()


# def main():
#     shifting_animation = ShiftingAnimation()
#     shifting_animation.color_set=[RED, ORANGE, YELLOW, BLACK]
#     shifting_animation.cycle_time = 3.0

#     strip = pixelstrip.PixelStrip(4, 64, brightness=BRIGHTNESS, auto_write=False)
#     strip.animation = shifting_animation

#     while True:
#         strip.draw()

# main()
