
#include <Wire.h>

// Tester code for i2c_animations.py.
// This Arduino program sends out a change-animation signal
// every five seconds.


const int I2C_ADDRESS = 0x41;
const int MAX_ANIMATIONS = 3;
const int MAX_STRIPS = 2;

void setup()
{
  Wire.begin();
  pinMode(LED_BUILTIN, OUTPUT);
}

byte strip_number = 0;
byte anim_number = 0;

void loop()
{
  strip_number = (strip_number + 1) % MAX_STRIPS;
  if (strip_number == 0) {
    anim_number = (anim_number + 1) % MAX_ANIMATIONS;
  }

  byte b = ((strip_number << 4) & 0xF0) + (anim_number & 0xF);
  Wire.beginTransmission(I2C_ADDRESS);
  Wire.write(b);
  Wire.endTransmission();

  digitalWrite(LED_BUILTIN, HIGH);
  delay(500);
  digitalWrite(LED_BUILTIN, LOW);

  delay(4500);
}
