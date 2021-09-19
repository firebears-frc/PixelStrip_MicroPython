import utime
import pixelstrip

# This is a a minimal example of an Animation.
# All Animations must define a draw().  It's also a good
# idea to define an __init__ function for initializing the 
# Animation and a reset function to reset things every time
# the Animation restarts. 

class MyAnimation(pixelstrip.Animation):
    def __init__(self):
        pixelstrip.Animation.__init__(self)
        # variable setup

    def reset(self, strip):
        # reset variables
        # set timeout if needed
        strip.clear()
        strip.show()

    def draw(self, strip, delta_time):
        # change pixel values
        strip.show()


# def main():
#     strip = pixelstrip.PixelStrip(4, 8)
#     strip.animation = MyAnimation()
#     while True:
#         strip.draw()
#         utime.sleep_ms(2)
#
# main()
