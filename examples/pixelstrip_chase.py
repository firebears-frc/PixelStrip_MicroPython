import utime
import pixelstrip

strip = pixelstrip.PixelStrip(4, 8)
strip.timeout = 0.0

color = (0, 128, 128, 0)
cycle_time = 2.0
current_pixel = -1

while True:
    if strip.is_timed_out():
        if current_pixel == -1:
            strip.fill((0, 0, 0, 0))
            strip.timeout = 0.5
            current_pixel = 0
        else:
            strip[current_pixel] = color
            strip.timeout = cycle_time / strip.n
            current_pixel = current_pixel + 1
            if current_pixel == strip.n:
                current_pixel = -1
        strip.show()
    utime.sleep_ms(2)

