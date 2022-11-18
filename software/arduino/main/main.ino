#include <Servo.h>

Servo rollServo;
Servo pitchServo;

String serialInput = "";
String rollDecode = "";
String pitchDecode = "";

int indexOfSpacer;

void setup() {
  //Setup Serial
  Serial.begin(9600);
  Serial.setTimeout(10);

  //Attach Servos
  rollServo.attach(A0);
  pitchServo.attach(A1);
}

void loop() {
  while (!Serial.available());//Wait for the send of a command
  delay(40);
  serialInput = Serial.readString();

  indexOfSpacer = serialInput.indexOf(":");

  rollDecode = serialInput.substring(0,indexOfSpacer);
  pitchDecode = serialInput.substring(indexOfSpacer+1, serialInput.length());
  
//  Serial.println(rollDecode);
//  Serial.println(pitchDecode);

  rollServo.write(rollDecode.toInt());
  pitchServo.write(pitchDecode.toInt());
}
