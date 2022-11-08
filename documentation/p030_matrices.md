# PixelStrip Matrices

We can do a lot of impressive animations with strips of WS2812B LEDs.  We can also use the same software to control 2-dimensional matrixes of LEDs.  Matrices are more dramatic, although they are also more expensive and they consume more electrical current.

![matrix_setup](./img/matrix_setup_33.jpg)

Wiring a matrix is the same as a pixel strip.  You'll need the same three support files loaded onto your Pico:  `npxl.py`, `pixelstrip.py`, and `colors.py`.  When creating a Python object to represent the matrix, you'll specify `height` and `width` parameters. You may also need to an `option` parameter, depending on how the matrix is wired and how it is positioned.

```python
strip = pixelstrip.PixelStrip(4, width=8, height=8, options={pixelstrip.MATRIX_TOP, pixelstrip.MATRIX_LEFT})
matrix[0, 0] = GREEN  
matrix[1, 3] = RED   # pixel colors are set by the row and column
```

Here's a simple matrix program:

```python
from utime import sleep_ms, sleep
from colors import *
import pixelstrip

matrix = pixelstrip.PixelStrip(4, width=8, height=8)
matrix.timeout = 0.0
i = 0

while True:
    if matrix.is_timed_out():
        matrix.clear()
        matrix[i, i] = BLUE
        matrix.show()
        i = (i + 1) % 8
        matrix.timeout = 0.7
```

You can break a complex program into smaller functions:

```python
from utime import sleep_ms, sleep
from colors import *
import pixelstrip

matrix = pixelstrip.PixelStrip(4, width=8, height=8)
matrix.timeout = 0.0
r = 0

def draw_vertical_line(m, row, color):
    for col in range(m.height):
        m[row, col] = color

while True:
    if matrix.is_timed_out():
        matrix.clear()
        draw_vertical_line(matrix, r, YELLOW)
        matrix.show()
        matrix.timeout = 0.5
        r = (r + 1) % matrix.width
```
