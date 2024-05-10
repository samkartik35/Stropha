#include <Servo.h>

Servo servoPan;  // Create servo object to control the pan
Servo servoTilt; // Create servo object to control the tilt

void setup() {
  // Attach the servos to digital pins
  servoPan.attach(9);   // Pan servo on digital pin 9
  servoTilt.attach(10); // Tilt servo on digital pin 10

  // Start serial communication at 9600 bps
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    // Read the incoming byte:
    String data = Serial.readStringUntil('\n'); // Read data until new line
    if (data.length() > 0) {
      int commaIndex = data.indexOf(','); // Find the position of the comma
      if (commaIndex != -1) {
        // Extract the pan angle before the comma
        int panAngle = data.substring(0, commaIndex).toInt();
        // Extract the tilt angle after the comma
        int tiltAngle = data.substring(commaIndex + 1).toInt();
        
        // Set servo angles
        servoPan.write(constrain(panAngle, 0, 180));  // Constrain angle to 0-180 degrees
        servoTilt.write(constrain(tiltAngle, 0, 180)); // Constrain angle to 0-180 degrees
      }
    }
  }
}
