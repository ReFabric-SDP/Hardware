#define sensor1 A4 // Sharp IR GP2Y0A41SK0F (4-30cm, analog)
#define sensor2 A3
#define sensor3 A2
#define sensor4 A1
// TODO: sensor1 should be top left, 2 should be top right, 3 bottom left

void setup() {
  Serial.begin(9600); // start the serial port
}

void loop() {
  
  // 5v
  float volt0 = analogRead(sensor1)*0.0048828125;  // value from sensor * (5/1024)
  int distance0 = 13*pow(volt0, -1); // worked out from datasheet graph

  float volt1 = analogRead(sensor2)*0.0048828125;
  int distance1 = 13*pow(volt1, -1); 

  float volt2 = analogRead(sensor3)*0.0048828125;
  int distance2 = 13*pow(volt2, -1); 

  float volt3 = analogRead(sensor4)*0.0048828125;
  int distance3 = 13*pow(volt3, -1); 

  // slow down serial port, but not too slow
  delay(200);

  Serial.print(distance0);
  Serial.print(" ");
  Serial.print(distance1);
  Serial.print(" ");
  Serial.print(distance2);
  Serial.print(" ");
  Serial.println(distance3);
  
}
