# PixelStrip Objects

`PixelStrip` software objects are interfaces to WS2812 RGB LED collections.
Each WS2812 strip will be connected to a specific pin on your Raspberry Pi Pico.
The strip will have a specific size (i.e. number of pixels).

---

## Constructors

```python
strip = pixelstrip.PixelStrip(pin, size)
```
Construct a `PixelStrip` for the given pin and size.

```python
strip = pixelstrip.PixelStrip(pin, n=8, brightness=1.0, auto_write=False)
```

Construct a `PixelStrip` for the given pin.  The strip size is given by the `n` parameter.  Other parameters are optional.

```python
strip = pixelstrip.PixelStrip(pin, width=16, height=8, brightness=1.0, auto_write=False, options=None)
```
Construct a `PixelStrip` for a pixel matrix of the given width and height.  The `brightness`, `auto_write`, and `options` parameters are optional.

The `options` parameter is important for specifying how your pixel matrix is wired and positioned.  If it is not `None`, then it should a Python set containing one or more of the following:
* `MATRIX_TOP`          Pixel 0 is at top of matrix
* `MATRIX_BOTTOM`       Pixel 0 is at bottom of matrix
* `MATRIX_LEFT`         Pixel 0 is at left of matrix
* `MATRIX_RIGHT`        Pixel 0 is at right of matrix
* `MATRIX_ROW_MAJOR`    Matrix is row major (horizontal)
* `MATRIX_COLUMN_MAJOR` Matrix is column major (vertical)
* `MATRIX_PROGRESSIVE`  Same pixel order across each line
* `MATRIX_ZIGZAG`       Pixel order reverses between lines

---

## Array Operations on PixelStrips

All `PixelStrip` objects can be treated as if they were [Python arrays](https://www.w3schools.com/python/python_arrays.asp), so you can set colors into strip at any given pixel number.  For instance, writing a color into `strip[0]` will change the color of the first pixel.  You can also read back the color by reading `strip[0]`.

Colors on the `PixelStrip` are represented as a three-number [Python tuple](https://www.w3schools.com/python/python_tuples.asp).  The three numbers give the amount of red, green, and blue in the color.  Each number should be in the range from 0 to 255.  Typically we use hexadecimal numbers, although you can also use normal decimal.

Examples:
```python
strip[0] = RED                 # Set the first pixel to be red
strip[1] = (0x00, 0xff, 0x00)  # Set the second pixel to be green
strip[2] = (255, 255, 0)       # Set the third pixel to be yellow
strip[2,6] = BLUE              # Set a pixel in the third column and seventh row of a matrix
```

---

## Properties

### n

```python
strip.n    # number of pixels on the strip
```
Reading `n` tells the total number of pixels on the strip.  Do not try to modify this property.

### width

```python
strip.width    # number of pixel columns in a matrix
```
The `width` and `height` properties give the dimensions of a matrix.  The `width` gives the number of pixels on the horizontal axis.  Do not try to modify this property.

### height

```python
strip.height    # number of pixel rows in a matrix
```
The `height` gives the number of pixels on the vertical axis.   If the given `PixelStrip` is not a matrix, then the height will be 1.  Do not try to modify these properties.

### animation

```python
strip.animation    # Animation object or None
```
Setting the `animation` property to `None` stops all animaton on the strip and clears all pixels.
Setting the `animation` property to an [Animation](doc_animation.md) object causes that animation to reset and started.  It is best not to assign the same `Animation` object to multiple strips.

### timeout

```python
strip.timeout    # Nmber of seconds
```
Setting the `timeout` property to a number of seconds means that the strip will be timed out that many
seconds in the future.  Setting `timeout` to `None` clears the timeout.

### brightness

```python
strip.brightness    # Relative brightness between 0.0 and 1.0
```
Setting `brightness` instantly changes the strips brightness.

### auto_write

```python
strip.auto_write    # Boolean value.
```
If `auto_write` is set to `True`, then changes are written automatically, without having to call the `show()` method.  By default, this property is `False`.

### wrap

```python
strip.wrap    # Boolean value.
```
If `wrap` is set to `True`, then specfiying indices outside the strip's range will be automatically be
wrapped forward or backward.   By default, this property is `False`.

---

## Methods

---

## Colors
