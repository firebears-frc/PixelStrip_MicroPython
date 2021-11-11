import time
from machine import Pin
from i2cp import i2cSlave
from pixelstrip import PixelStrip, current_time
from animation_pulse import PulseAnimation

I2C_ADDRESS = 0x41
BRIGHTNESS = 0.5

# List of Animations
animation = [
    PulseAnimation(),
    PulseAnimation([(0, 136, 0, 0), (64, 64, 0, 0)]),
    PulseAnimation([(0, 0, 136, 0), (0, 64, 64, 0)]),
]

# List of PixelStrips
strip = [
    PixelStrip(4, 12, brightness=BRIGHTNESS),
    PixelStrip(5, 8, brightness=BRIGHTNESS),
    PixelStrip(6, 12, brightness=BRIGHTNESS),
    PixelStrip(8, 12, brightness=BRIGHTNESS)
]

# The built-in LED will turn on for half a second after every message
led = Pin(25, Pin.OUT)
led.value(False)

i2c_slave = i2cSlave(0,sda=16,scl=17,slave_address=I2C_ADDRESS)

def receive_message():
    global i2c_slave
    if i2c_slave.any():
        b = i2c_slave.get()
        strip_num = int((b & 0xF0) >> 4)
        anim_num = int(b & 0x0F)
        return (strip_num, anim_num)
    else:
        return None

def main():
    global strip, led
    blink(3)
    for s in strip:
        s.clear()
        s.show()
    last_msg_time = 0.0
    while True:
        for s in strip:
            s.draw()
        message = receive_message()
        if message:
            strip_num = message[0]
            anim_num = message[1]
            strip[strip_num].animation = animation[anim_num]
            last_msg_time = current_time()
        led.value(current_time() < last_msg_time + 0.5)

def blink(i):
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

main()



