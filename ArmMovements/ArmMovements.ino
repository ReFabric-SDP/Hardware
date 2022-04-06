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
  DROP_OFF_5,
  READY = 98,
  STANDBY = 99
};

// pickup includes 2 steps: reaching down, and raising to camera
void raise_to_camera() {
  Braccio.ServoMovement(20,          90,  85, 40, 20, 90, 73); // move backwards a bit to not hit back of box
  Braccio.ServoMovement(20,          60,  90, 80, 50, 90, 73);  // move for camera
}

void to_standby_position() {
  Braccio.ServoMovement(20,          90,  90, 90, 0, 90,  73);
}

void to_ready_position() {
    // same as begin position
    Braccio.ServoMovement(20,          90,  130, 20, 90, 0, 73);
}

// tlu = top left upper, brl = bottom right lower
void pickup_action_tlu() {
Braccio.ServoMovement(20,          70,  50, 60, 30, 90,  0);
Braccio.ServoMovement(20,          70,  50, 60, 30, 90,  73);
raise_to_camera();
to_standby_position();
}

void pickup_action_tll() {
Braccio.ServoMovement(20,          70,  20, 80, 30, 90,  0);
Braccio.ServoMovement(20,          70,  20, 80, 30, 90,  73);
raise_to_camera();
to_standby_position();

}

void pickup_action_tru() {
Braccio.ServoMovement(20,         110,  50, 60, 30, 90,  0);
Braccio.ServoMovement(20,         110,  50, 60, 30, 90,  73);
raise_to_camera();
to_standby_position();
}


void pickup_action_trl() {
Braccio.ServoMovement(20,          110,  20, 80, 30, 90,  0);
Braccio.ServoMovement(20,          110,  20, 80, 30, 90,  73);
raise_to_camera();
to_standby_position();
}

void pickup_action_blu() {
  Braccio.ServoMovement(20,          70,  50, 70, 0, 90,  0);  
  Braccio.ServoMovement(20,          70,  50, 70, 0, 90,  73); 
  raise_to_camera();
  to_standby_position();
}

void pickup_action_bll() {
  Braccio.ServoMovement(20,          70,  20, 50, 30, 90,  0);  
  Braccio.ServoMovement(20,          70,  20, 50, 30, 90,  73); 
  raise_to_camera();
  to_standby_position();
}

void pickup_action_bru() {
  Braccio.ServoMovement(20,          110,  50, 70, 0, 90,  0);  
  Braccio.ServoMovement(20,          110,  50, 70, 0, 90,  73); 
  raise_to_camera();
  to_standby_position();
}

void pickup_action_brl() {
  Braccio.ServoMovement(20,          110,  20, 50, 30, 90,  0);  
  Braccio.ServoMovement(20,          110,  20, 50, 30, 90,  73); 
  raise_to_camera();
  to_standby_position();
}

void drop_off_action_01() {
  Braccio.ServoMovement(20,          0,  90, 90, 0, 90,  73);
  Braccio.ServoMovement(20,          0,  70, 80, 10, 90,  73);
  Braccio.ServoMovement(20,          0,  70, 80, 10, 90,  0);

}

void drop_off_action_34() {
  Braccio.ServoMovement(20,          180,  90, 90, 0, 90,  73);
  Braccio.ServoMovement(20,          180,  70, 80, 10, 90,  73);
  Braccio.ServoMovement(20,          180,  70, 80, 10, 90,  0);
}

void drop_off_action_2() {
  Braccio.ServoMovement(20,          0,  90, 90, 0, 90,  73);
  Braccio.ServoMovement(20,          0,  70, 80, 10, 90,  73);
  Braccio.ServoMovement(20,          0,  70, 80, 10, 90,  0);

}

void drop_off_action_5() {
  Braccio.ServoMovement(20,          180,  90, 90, 0, 90,  73);
  Braccio.ServoMovement(20,          180,  70, 80, 10, 90,  73);
  Braccio.ServoMovement(20,          180,  70, 80, 10, 90,  0);
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

      case DROP_OFF_01: drop_off_action_01(); Serial.write((unsigned int)command); break;
      case DROP_OFF_2: drop_off_action_2(); Serial.write((unsigned int)command); break;
      case DROP_OFF_34: drop_off_action_34(); Serial.write((unsigned int)command); break;
      case DROP_OFF_5: drop_off_action_5(); Serial.write((unsigned int)command); break;

      case STANDBY: to_standby_position(); Serial.write((unsigned int)command); break;
      case READY: to_ready_position(); Serial.write((unsigned int)command); break;
      default: Serial.write(88); break;  // junk value
    }
  }
}
