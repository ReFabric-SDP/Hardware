// For Sharp GP2D12
//const int IR_SENSOR = 0;    // Sensor is connected to the analog A0
//
//void setup() { 
//   Serial.begin(9600);    // Start serial port communication 
//} 
// 
//void loop() { 
//   // Read the IR sensor 
//   int intSensorInput = analogRead(IR_SENSOR);
//   // Calculated value
//   float fltSensorCalculation = (6787.0 / (intSensorInput - 3.0)) - 4.0; 
//
//   //Calculate distance in cm and print to screen
//   Serial.print(fltSensorCalculation);
////   Serial.println(intSensorInput);
//   Serial.println(" cm");
//   delay(200);
//}


// For Sharp IR GP2Y0A41SK0F
// http://tinkcore.com/sharp-ir-gp2y0a41-skf/

#define sensor A0 // Sharp IR GP2Y0A41SK0F (4-30cm, analog)

void setup() {
  Serial.begin(9600); // start the serial port
}

void loop() {
  
  // 5v
  float volts = analogRead(sensor)*0.0048828125;  // value from sensor * (5/1024)
  int distance = 13*pow(volts, -1); // worked out from datasheet graph
  delay(1000); // slow down serial port 
  
  if (distance <= 30){
    Serial.println(distance);   // print the distance
  }
}
