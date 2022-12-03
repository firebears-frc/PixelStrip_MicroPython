import time
from machine import Pin
from i2cp import I2cPerf
from pixelstrip import PixelStrip, current_time
from animation_pulse import PulseAnimation

I2C_ADDRESS = 0x41
BRIGHTNESS = 0.5

# List of Animations
animation = [
    PulseAnimation(),
    PulseAnimation([(0, 136, 0), (64, 64, 0)]),
    PulseAnimation([(0, 0, 136), (0, 64, 64)]),
]

# List of PixelStrips
strip = [
    PixelStrip(4, 12, brightness=BRIGHTNESS),
    PixelStrip(5, 8, brightness=BRIGHTNESS),
    PixelStrip(8, 12, brightness=BRIGHTNESS),
    PixelStrsip(9, 12, brightness=BRIGHTNESS)
]

# The built-in LED will turn on for half a second after every message
led = Pin(25, Pin.OUT)
led.value(False)

i2c = I2cPerf(1,sda=6,scl=7,address=I2C_ADDRESS)

def receive_message():
    """
    Receive one byte on I2C bus.  Translate to strip and animation number.
    """
    global i2c
    if i2c.available():
        b = i2c.read()
        strip_num = int((b & 0xF0) >> 4)
        anim_num = int(b & 0x0F)
        return (strip_num, anim_num)
    else:
        return None

def set_animation(strip_num, anim_num):
    """
    Set the animation on one PixelStrip to be one Animation.
    If anim_num is too large, stop animation and clear strip.
    """
    if anim_num < len(animation):
        strip[strip_num].animation = animation[anim_num]
    else:
        strip[strip_num].animation = None

def blink(i):
    """
    Blink onboard LED and also each PixelStrip.
    This demonstrates that the program is active and all strips are connected.
    """
    for _ in range(i):
        led.toggle()
        for s in strip:
            s[0] = (128, 0, 0, 0)
            s.show()
        time.sleep(0.2)
        led.toggle()
        for s in strip:
            s.clear()
            s.show()
        time.sleep(0.2)

def main():
    global strip, led
    for s in strip:
        s.reset()
    blink(3)
    last_msg_time = 0.0
    while True:
        for s in strip:
            s.draw()
        message = receive_message()
        if message:
            strip_num = message[0]
            anim_num = message[1]
            set_animation(strip_num, anim_num)
            last_msg_time = current_time()
        led.value(current_time() < last_msg_time + 0.5)

main()




