#include <Braccio.h>
#include <Servo.h>

Servo base;
Servo shoulder;
Servo elbow;
Servo wrist_rot;
Servo wrist_ver;
Servo gripper;

enum actions {
  TOP_LEFT_UPPER = 1,
  TOP_LEFT_LOWER,
  TOP_RIGHT_UPPER,
  TOP_RIGHT_LOWER,
  BOTTOM_LEFT_UPPER,
  BOTTOM_LEFT_LOWER,
  BOTTOM_RIGHT_UPPER,
  BOTTOM_RIGHT_LOWER,
  DROP_OFF_01,
  DROP_OFF_34,
  DROP_OFF_2,
  DROP_OFF_5
}

// pickup includes 2 steps: reaching down, and raising to camera
void raise_to_camera() {

}

// tlu = top left upper, brl = bottom right lower
void pickup_action_tlu() {

}

void pickup_action_tll() {

}

void pickup_action_tru() {

}

void pickup_action_trl() {

}

void pickup_action_blu() {

}

void pickup_action_bll() {

}

void pickup_action_bru() {

}

void pickup_action_brl() {

}


void drop_off_action_01() {
  // TODO, not last row, rhs, command should be '9'

}

void drop_off_action_34() {
  // TODO, not last row, lhs, command should be '10'

}

void drop_off_action_2() {
  // TODO, last row, rhs, command should be '11'

}

void drop_off_action_5() {
  // TODO, last row, lhs, command should be '12'

}


void setup() {
  //Initialization functions and set up the initial position for Braccio
  //All the servo motors will be positioned in the "safety" position:
  //Base (M1):90 degrees
  //Shoulder (M2): 45 degrees
  //Elbow (M3): 180 degrees
  //Wrist vertical (M4): 180 degrees
  //Wrist rotation (M5): 90 degrees
  //gripper (M6): 10 degrees

pinMode(12, OUTPUT);    //you need to set HIGH the pin 12
digitalWrite(12, HIGH);
Braccio.begin(SOFT_START_DISABLED);
//Braccio.begin(0);
Serial.begin(9600);

}

void loop() {
   /*
   Step Delay: a milliseconds delay between the movement of each servo.  Allowed values from 10 to 30 msec.
   M1=base degrees. Allowed values from 0 to 180 degrees
   M2=shoulder degrees. Allowed values from 15 to 165 degrees
   M3=elbow degrees. Allowed values from 0 to 180 degrees
   M4=wrist vertical degrees. Allowed values from 0 to 180 degrees
   M5=wrist rotation degrees. Allowed values from 0 to 180 degrees
   M6=gripper degrees. Allowed values from 10 to 73 degrees. 10: the toungue is open, 73: the gripper is closed.
  */

  // (step delay, M1, M2, M3, M4, M5, M6);
  if (Serial.available() > 0) {
    actions command = (actions) (unsigned int) Serial.read();
    switch (command) {
      case TOP_LEFT_UPPER: pickup_action_tlu(); Serial.write((unsigned int)command); break;
      case TOP_LEFT_LOWER: pickup_action_tll(); Serial.write((unsigned int)command); break;
      case TOP_RIGHT_UPPER: pickup_action_tru(); Serial.write((unsigned int)command); break;
      case TOP_RIGHT_LOWER: pickup_action_trl(); Serial.write((unsigned int)command); break;
      case BOTTOM_LEFT_UPPER: pickup_action_blu(); Serial.write((unsigned int)command); break;
      case BOTTOM_LEFT_LOWER: pickup_action_bll(); Serial.write((unsigned int)command); break;
      case BOTTOM_RIGHT_UPPER: pickup_action_bru(); Serial.write((unsigned int)command); break;
      case BOTTOM_RIGHT_LOWER: pickup_action_brl(); Serial.write((unsigned int)command); break;
      default: Serial.write(99); break;  // junk value
    }
  }
}