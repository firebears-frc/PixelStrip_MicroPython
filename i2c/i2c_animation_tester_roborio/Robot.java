package frc.robot;

import edu.wpi.first.wpilibj.TimedRobot;
import edu.wpi.first.wpilibj.XboxController;
import edu.wpi.first.wpilibj.GenericHID.Hand;
import edu.wpi.first.wpilibj.I2C;
import edu.wpi.first.wpilibj.I2C.Port;

public class Robot extends TimedRobot {

  public static int I2C_ADDRESS = 0x41;
  public static final int MAX_ANIMATIONS = 3;
  public static final int MAX_STRIPS = 4;

  private byte[] currentAnimation = new byte[MAX_STRIPS];
  private byte[] nextAnimation = new byte[MAX_STRIPS];
  private int myStrip = 0;
  private int myAnim = 0;
  private byte[] dataOut = new byte[1];

  private XboxController xbox = null;
  private I2C i2c = null;

  @Override
  public void robotInit() {
    xbox = new XboxController(0);
    i2c = new I2C(Port.kOnboard, I2C_ADDRESS);
    resetAnimations();
  }

  @Override
  public void teleopPeriodic() {
    if (xbox.getBumperPressed(Hand.kLeft)) {
      myAnim = (myAnim + 1) % MAX_ANIMATIONS;
      setAnimation(myStrip, myAnim);
    } else if (xbox.getBumperPressed(Hand.kRight)) {
      resetAnimations();
    } else if (xbox.getYButtonPressed()) {
      myStrip = 0;
    } else if (xbox.getBButtonPressed()) {
      myStrip = 1;
    } else if (xbox.getAButtonPressed()) {
      myStrip = 2;
    } else if (xbox.getXButtonPressed()) {
      myStrip = 3;
    }
    sendAllAnimations();
  }

  private void resetAnimations() {
    for (int s = 0; s < MAX_STRIPS; s++) {
      nextAnimation[s] = (byte)0x0f;
      currentAnimation[s] = 0;
    }
    myStrip = 0;
    myAnim = 0;
  }

  private void setAnimation(int stripNumber, int animNumber) {
    Integer b = Integer.valueOf(((stripNumber << 4) & 0xF0) | (animNumber & 0x0F));
    nextAnimation[stripNumber] = b.byteValue();
  }

  private void sendAllAnimations() {
    for (int s = 0; s < MAX_STRIPS; s++) {
      if (nextAnimation[s] != currentAnimation[s]) {
        sendOneAnimation(s);
        currentAnimation[s] = nextAnimation[s];
      }
    }
  }

  private void sendOneAnimation(int stripNumber) {
    dataOut[0] = nextAnimation[stripNumber];
    i2c.writeBulk(dataOut, dataOut.length);
  }
}
