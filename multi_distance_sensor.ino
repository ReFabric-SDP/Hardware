#define sensor0 A0 // Sharp IR GP2Y0A41SK0F (4-30cm, analog)
#define sensor1 A1
#define sensor2 A2
#define sensor3 A3


void setup() {
  Serial.begin(9600); // start the serial port
}

void loop() {
  
  // 5v
  float volt0 = analogRead(sensor0)*0.0048828125;  // value from sensor * (5/1024)
  int distance0 = 13*pow(volt0, -1); // worked out from datasheet graph

  float volt1 = analogRead(sensor1)*0.0048828125;  
  int distance1 = 13*pow(volt1, -1); 

  float volt2 = analogRead(sensor2)*0.0048828125;  
  int distance2 = 13*pow(volt2, -1); 

  float volt3 = analogRead(sensor3)*0.0048828125; 
  int distance3 = 13*pow(volt3, -1); 

  // slow down serial port
  delay(1000); 

  Serial.print("Sensor 0: ");
  Serial.print(distance0);
  Serial.println(" cm");

  Serial.print("Sensor 1: ");
  Serial.print(distance1);
  Serial.println(" cm");

  Serial.print("Sensor 2: ");
  Serial.print(distance2);
  Serial.println(" cm");

  Serial.print("Sensor 3: ");
  Serial.print(distance3);
  Serial.println(" cm");

  Serial.println("----------------------------------");
}
