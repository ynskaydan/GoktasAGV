#include <QTRSensors.h>

#define Kp 0.1 
#define Kd 1.8 
#define rightMaxSpeed 84
#define leftMaxSpeed 85
#define rightBaseSpeed 65 
#define leftBaseSpeed 66 


#define rightMotor1 2
#define rightMotor2 3
#define rightMotorE 9
#define leftMotor1 4
#define leftMotor2 5
#define leftMotorE 10


QTRSensors qtr;

const uint8_t SensorCount = 16;
unsigned int sensorValues[SensorCount];



void setup()
{
  qtr.setTypeRC();
  qtr.setSensorPins((const uint8_t[]){34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49}, SensorCount);
  qtr.setEmitterPin(2);
  pinMode(rightMotor1, OUTPUT);
  pinMode(rightMotor2, OUTPUT);
  pinMode(rightMotorE, OUTPUT);
  pinMode(leftMotor1, OUTPUT);
  pinMode(leftMotor2, OUTPUT);
  pinMode(leftMotorE, OUTPUT);


  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH); // turn on Arduino's LED to indicate we are in calibration mode


  int i;
  for (int i = 0; i < 100; i++) { 
    if ( i  < 25 || i >= 75 ) {
      turn_right();
    } 
    else {
      turn_left();
    }
    qtr.calibrate();
    delay(20);
  }
  wait(); 
  digitalWrite(LED_BUILTIN, LOW); 

  delay(1000); 
}
int lastError = 0;
void loop()
{
  // read calibrated sensor values and obtain a measure of the line position
  unsigned int position = qtr.readLineBlack(sensorValues);


  int error = position - 7500;
  int motorSpeed = Kp * error + Kd * (error - lastError);
  lastError = error;
  int rightMotorSpeed = rightBaseSpeed + motorSpeed;
  int leftMotorSpeed = leftBaseSpeed - motorSpeed;
  if (rightMotorSpeed > rightMaxSpeed ) rightMotorSpeed = rightMaxSpeed;
  if (leftMotorSpeed > leftMaxSpeed ) leftMotorSpeed = leftMaxSpeed;
  if (rightMotorSpeed < 0) rightMotorSpeed = 0;
  if (leftMotorSpeed < 0) leftMotorSpeed = 0;
  

    digitalWrite(rightMotor1, HIGH);
    digitalWrite(rightMotor2, LOW);
    analogWrite(rightMotorE, rightMotorSpeed);

    digitalWrite(leftMotor1, HIGH);
    digitalWrite(leftMotor2, LOW);
    analogWrite(leftMotorE, leftMotorSpeed);
  
}
void wait() {
      digitalWrite(rightMotor1,LOW);
    digitalWrite(rightMotor2, LOW);
   

    digitalWrite(leftMotor1, LOW);
    digitalWrite(leftMotor2, LOW);
    
}
void turn_left() {
      digitalWrite(rightMotor1,HIGH);
    digitalWrite(rightMotor2, LOW);
    analogWrite (rightMotorE,rightBaseSpeed); 

    digitalWrite(leftMotor1, LOW);
    digitalWrite(leftMotor2, HIGH);
    analogWrite (leftMotorE,leftBaseSpeed);
}
void turn_right() {
      digitalWrite(rightMotor1,LOW);
    digitalWrite(rightMotor2, HIGH);
    analogWrite (rightMotorE,rightBaseSpeed);   

    digitalWrite(leftMotor1, HIGH);
    digitalWrite(leftMotor2, LOW);
    analogWrite (leftMotorE,leftBaseSpeed);    
}