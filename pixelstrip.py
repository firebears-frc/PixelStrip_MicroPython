import utime
import npxl as neopixel


def current_time():
    """
    Returns the current time in seconds.
    """
    return utime.ticks_ms() / 1000.0


MATRIX_TOP = 0x01           # Pixel 0 is at top of matrix
MATRIX_BOTTOM = 0x02        # Pixel 0 is at bottom of matrix
MATRIX_LEFT = 0x04          # Pixel 0 is at left of matrix
MATRIX_RIGHT = 0x08         # Pixel 0 is at right of matrix
MATRIX_ROW_MAJOR = 0x10     # Matrix is row major (horizontal)
MATRIX_COLUMN_MAJOR = 0x20  # Matrix is column major (vertical)
MATRIX_PROGRESSIVE = 0x40   # Same pixel order across each line
MATRIX_ZIGZAG = 0x80        # Pixel order reverses between lines


class PixelStrip(neopixel.NeoPixel):
    """
    Subclass of NeoPixel, but supporting Animations.
    """

    def __init__(
            self, pin, n=8, width=None, height=None, brightness=1.0, options=None, auto_write=False
    ):
        self._options = { MATRIX_PROGRESSIVE, MATRIX_ROW_MAJOR, MATRIX_TOP, MATRIX_LEFT }
        self.width = n
        self.height = 1
        if width is not None and height is not None:
            n = width * height
            self.width = width
            self.height = height
        if options is not None:
            self._options = options
        neopixel.NeoPixel.__init__(
            self,
            pin,
            n,
            brightness=brightness,
            auto_write=auto_write,
            pixel_order=None,
        )
        self._timeout = None
        self._animation = None
        self._prev_time = current_time()
        self.wrap = False

    def draw(self):
        """
        Draw one cycle of the strip animation.
        """
        if self._animation is not None:
            delta_time = current_time() - self._prev_time
            self._animation.draw(self, delta_time)
            self._prev_time = current_time()

    def reset(self):
        """
        Reset the strip animation.
        """
        self._prev_time = current_time()
        if self._animation is not None:
            self._animation.reset(self)
        else:
            self.clear()

    def clear(self):
        """
        Turn all pixels off.
        """
        self.fill((0, 0, 0))
        self.show()

    def __setitem__(self, index, color):
        if type(index) is tuple:
            nn = self._translate_pixel(index[0], index[1])
        else:
            nn = index
        if self.wrap:
            while nn < 0:
                nn += len(self)
            while nn >= len(self):
                nn -= len(self)
        super().__setitem__(nn, color)

    def _translate_pixel(self, x, y):
        xx = x
        yy = y

        if MATRIX_TOP in self._options and MATRIX_RIGHT in self._options:
            xx = y
            yy = self.height - (x + 1)
        elif MATRIX_BOTTOM in self._options and MATRIX_RIGHT in self._options:
            xx = self.width - (x + 1)
            yy = self.height - (y + 1)
        elif MATRIX_BOTTOM in self._options and MATRIX_LEFT in self._options:
            xx = self.width - (y + 1)
            yy = x

        if MATRIX_ZIGZAG in self._options:
            if MATRIX_COLUMN_MAJOR in self._options and xx % 2 == 1:
                yy = self.height - (yy + 1)
            elif MATRIX_ROW_MAJOR in self._options and yy % 2 == 1:
                xx = self.width - (xx + 1)

        if MATRIX_COLUMN_MAJOR in self._options:
            return xx * self.height + yy
        else:
            return xx + yy * self.width

    @property
    def animation(self):
        return self._animation

    @animation.setter
    def animation(self, anim):
        self._animation = anim
        if self._animation is not None:
            self._animation.reset(self)
        else:
            self.clear()

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, t):
        """
        Set or reset a timeout (in seconds) on this PixelStrip.
        Setting with None cancels the timeout.
        """
        if t < 0 or t is None:
            self._timeout = None
        else:
            self._timeout = current_time() + t

    def is_timed_out(self):
        """
        Determine if the timeout has been reached.
        """
        if self._timeout is None:
            return False
        else:
            return current_time() >= self._timeout


class Animation:
    """
    Base class for all animations.
    """

    def __init__(self, name=None):
        self._timeout = None
        self._name = name

    def __repr__(self):
        t = self.__class__.__name__
        n = "" if self._name is None else self._name
        return "{}({})".format(t, n)

    def __str__(self):
        t = self.__class__.__name__
        return t if self._name is None else self._name

    def reset(self, strip):
        """
        Reset this animation for the given pixel strip.
        """
        pass

    def draw(self, strip, delta_time):
        """
        Draw one cycle of this animation against the given pixel strip.
        The delta_time is the number of seconds since the last draw call.
        """
        pass

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, t):
        """
        Set or reset a timeout (in seconds) on this PixelStrip.
        Setting with None cancels the timeout.
        """
        if t < 0 or t is None:
            self._timeout = None
        else:
            self._timeout = current_time() + t

    def is_timed_out(self):
        """
        Determine if the timeout has been reached.
        """
        if self._timeout is None:
            return False
        else:
            return current_time() >= self._timeout
