#include <Servo.h>

Servo rollServo;
Servo pitchServo;

String serialInput = "";
String rollDecode = "";
String pitchDecode = "";

int rollServoMin = 50, rollServoMax = 100;
int pitchServoMin = 50, pitchServoMax = 100;

int indexOfSpacer;

//OpenCV Constants
int viewportSize[2] = {640, 480};

//PID Varibles
double time;
int period = 50;//ms
double rollSetPoint = 320; //Influnces X Coordinate
double pitchSetPoint = 240; //Influnces Y Coordinate
double errorX, errorY, errorXprev, errorYprev;
double Kp = 1;
double Ki = 0;
double Kd = 0;
double xPID_K, xPID_I, xPID_D, xPID_Total;
double yPID_K, yPID_I, yPID_D, yPID_Total;


void setup() {
  //Setup Serial
  Serial.begin(9600);
  Serial.setTimeout(10);

  //Attach Servos
  rollServo.attach(A0);
  pitchServo.attach(A1);

  time = millis();
}

void loop() {
  while (!Serial.available() && millis() < time+period);//Wait for period and Message
  serialInput = Serial.readString();

  indexOfSpacer = serialInput.indexOf(":");

  rollDecode = serialInput.substring(0,indexOfSpacer);
  pitchDecode = serialInput.substring(indexOfSpacer+1, serialInput.length());

  // PID Calculation  
  errorX = rollSetPoint - rollDecode.toInt();
  errorY = pitchSetPoint - pitchDecode.toInt();

  xPID_K = errorX * Kp;
  yPID_K = errorY * Kp;
  
  xPID_D = ((errorX - errorXprev)/period) * Kd;
  yPID_D = ((errorY - errorYprev)/period) * Kd;

  xPID_I += errorX * Ki * period;
  yPID_I += errorY * Ki * period;

  xPID_Total = xPID_K + xPID_I + xPID_D;
  yPID_Total = yPID_K + yPID_I + yPID_D;

  //Mapping PID
  xPID_Total = map(xPID_Total, -viewportSize[0]/2*Kp, viewportSize[0]/2*Kp, rollServoMin, rollServoMax);
  yPID_Total = map(yPID_Total, -viewportSize[1]/2*Kp, viewportSize[1]/2*Kp, pitchServoMin, pitchServoMax);

  rollServo.write(xPID_Total);
  pitchServo.write(yPID_Total);

  //For 4 servos
//  servo1.write(-xPID_Total/2);
//  servo2.write(-yPID_Total/2);
//  servo3.write(xPID_Total/2);
//  servo4.write(yPID_Total/2);
}
