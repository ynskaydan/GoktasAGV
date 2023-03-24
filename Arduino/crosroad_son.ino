#include <QTRSensors.h>

#define Kp 0.3
#define Kd 2.0
#define rightMaxSpeed 75
#define leftMaxSpeed 75
#define rightBaseSpeed 65
#define leftBaseSpeed 65

#define leapTime 250
#define leftMotor1 4
#define leftMotor2 5
#define rightMotor1 2
#define rightMotor2 3
#define leftMotorE 10
#define rightMotorE 9

#define led 13

int donushizi = 75;
unsigned int sensors[16];
QTRSensors qtr;

const uint8_t SensorCount = 16;
unsigned int sensorValues[SensorCount];
unsigned int posit;

void setup() {
  qtr.setTypeRC();
  qtr.setSensorPins((const uint8_t[]){ 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49 }, SensorCount);

  pinMode(leftMotor1, OUTPUT);
  pinMode(leftMotor2, OUTPUT);
  pinMode(rightMotor1, OUTPUT);
  pinMode(rightMotor2, OUTPUT);
  pinMode(led, OUTPUT);
  Serial.begin(9600);



  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);

  int i;
  for (int i = 0; i < 100; i++) {
    if (i < 25 || i >= 75) {
      turn_right();
    } else {
      turn_left();
    }
    qtr.calibrate();
    delay(20);
  }
  wait();
  digitalWrite(LED_BUILTIN, LOW);

  delay(3000);
}
void loop() {

  qtr.read(sensors);
  for (int i = 0; i < 16; i++)
  {
    Serial.print(sensors[i]);
    Serial.print("\t");
  }
  Serial.println();
 if (sensors[15] > 500 && sensors[0] < 500) {
    Serial.println("Sola L kavşak algılandı...");
    delay(2000);
    turn_left();
    ilerle();
  }
  else if (sensors[0] > 500 && sensors[15] < 500) {
    Serial.println("Sağa L kavşak algılandı...");
    delay(2000);
    turn_right();
    ilerle();
  }else if (sensors[0] > 500 && sensors[15] > 500 && (sensors[7]> 500 && sensors[8]>500)) {
    Serial.println("T kavşak algılandı");
    delay(2000);
    turn_left();
    ilerle();
  }
  else {
    ilerle();
    Serial.println("Düz devam ediliyor.");
  }
}


void turn_left() {
  digitalWrite(rightMotor1, HIGH);
  digitalWrite(rightMotor2, LOW);
  analogWrite(rightMotorE, 90);

  digitalWrite(leftMotor1, LOW);
  digitalWrite(leftMotor2, HIGH);
  analogWrite(leftMotorE, 90);
}
void turn_right() {
  digitalWrite(rightMotor1, LOW);
  digitalWrite(rightMotor2, HIGH);
  analogWrite(rightMotorE, 90);

  digitalWrite(leftMotor1, HIGH);
  digitalWrite(leftMotor2, LOW);
  analogWrite(leftMotorE, 90);
}
void turnLeft() {


  while (digitalRead(sensors[7]) > 200 || digitalRead(sensors[8]) > 200) {
    digitalWrite(leftMotor1, LOW);
    digitalWrite(leftMotor2, HIGH);
    digitalWrite(rightMotor1, HIGH);
    digitalWrite(rightMotor2, LOW);
    analogWrite(rightMotorE, donushizi);
    analogWrite(leftMotorE, donushizi);
    delay(5);
    digitalWrite(leftMotor1, LOW);
    digitalWrite(leftMotor2, LOW);
    digitalWrite(rightMotor1, LOW);
    digitalWrite(rightMotor2, LOW);
    delay(2);
  }
  while (digitalRead(sensors[8]) < 200) {
    digitalWrite(leftMotor1, LOW);
    digitalWrite(leftMotor2, HIGH);
    digitalWrite(rightMotor1, HIGH);
    digitalWrite(rightMotor2, LOW);
    analogWrite(rightMotorE, donushizi);
    analogWrite(leftMotorE, donushizi);
    delay(4);
    digitalWrite(leftMotor1, LOW);
    digitalWrite(leftMotor2, LOW);
    digitalWrite(rightMotor1, LOW);
    digitalWrite(rightMotor2, LOW);
    delay(1);
  }
  while (digitalRead(sensors[7]) < 200) {
    digitalWrite(leftMotor1, LOW);
    digitalWrite(leftMotor2, HIGH);
    digitalWrite(rightMotor1, HIGH);
    digitalWrite(rightMotor2, LOW);
    analogWrite(rightMotorE, donushizi);
    analogWrite(leftMotorE, donushizi);
    delay(4);
    digitalWrite(leftMotor1, LOW);
    digitalWrite(leftMotor2, LOW);
    digitalWrite(rightMotor1, LOW);
    digitalWrite(rightMotor2, LOW);
    delay(1);
  }


}  //voidturnleft
void turnRight() {

  while (digitalRead(sensors[8]) > 200 || digitalRead(sensors[7]) > 200) {
    digitalWrite(leftMotor1, LOW);
    digitalWrite(leftMotor2, HIGH);
    digitalWrite(rightMotor1, HIGH);
    digitalWrite(rightMotor2, LOW);
    analogWrite(rightMotorE, donushizi);
    analogWrite(leftMotorE, donushizi);
    delay(5);
    digitalWrite(leftMotor1, LOW);
    digitalWrite(leftMotor2, LOW);
    digitalWrite(rightMotor1, LOW);
    digitalWrite(rightMotor2, LOW);
    delay(2);
  }

  while (digitalRead(sensors[7]) < 200) {
    digitalWrite(leftMotor1, HIGH);
    digitalWrite(leftMotor2, LOW);
    digitalWrite(rightMotor1, LOW);
    digitalWrite(rightMotor2, HIGH);
    analogWrite(rightMotorE, donushizi);
    analogWrite(leftMotorE, donushizi);
    delay(4);
    digitalWrite(leftMotor1, LOW);
    digitalWrite(leftMotor2, LOW);
    digitalWrite(rightMotor1, LOW);
    digitalWrite(rightMotor2, LOW);
    delay(1);
  }
  while (digitalRead(sensors[8]) < 200) {
    digitalWrite(leftMotor1, HIGH);
    digitalWrite(leftMotor2, LOW);
    digitalWrite(rightMotor1, LOW);
    digitalWrite(rightMotor2, HIGH);
    analogWrite(rightMotorE, donushizi);
    analogWrite(leftMotorE, donushizi);
    delay(4);
    digitalWrite(leftMotor1, LOW);
    digitalWrite(leftMotor2, LOW);
    digitalWrite(rightMotor1, LOW);
    digitalWrite(rightMotor2, LOW);
    delay(1);
  }
}  //voidturnright
void ilerle() {
  unsigned int position = qtr.readLineBlack(sensorValues);

  int lastError = 0;
  int error = position - 7500;
  int motorSpeed = Kp * error + Kd * (error - lastError);
  lastError = error;
  int rightMotorSpeed = rightBaseSpeed + motorSpeed;
  int leftMotorSpeed = leftBaseSpeed - motorSpeed;
  if (rightMotorSpeed > rightMaxSpeed) rightMotorSpeed = rightMaxSpeed;
  if (leftMotorSpeed > leftMaxSpeed) leftMotorSpeed = leftMaxSpeed;
  if (rightMotorSpeed < 0) rightMotorSpeed = 0;
  if (leftMotorSpeed < 0) leftMotorSpeed = 0;


  digitalWrite(rightMotor1, HIGH);
  digitalWrite(rightMotor2, LOW);
  analogWrite(rightMotorE, rightMotorSpeed);

  digitalWrite(leftMotor1, HIGH);
  digitalWrite(leftMotor2, LOW);
  analogWrite(leftMotorE, leftMotorSpeed);
}


void turnAround() {
  digitalWrite(leftMotor1, HIGH);
  digitalWrite(leftMotor2, LOW);
  digitalWrite(rightMotor1, HIGH);
  digitalWrite(rightMotor2, LOW);
  analogWrite(rightMotorE, rightBaseSpeed);
  analogWrite(leftMotorE, leftBaseSpeed);
  delay(leapTime);
  while (digitalRead(sensors[7]) < 200) {
    digitalWrite(leftMotor1, LOW);
    digitalWrite(leftMotor2, HIGH);
    digitalWrite(rightMotor1, HIGH);
    digitalWrite(rightMotor2, LOW);
    analogWrite(rightMotorE, donushizi);
    analogWrite(leftMotorE, donushizi);
    delay(5);
    digitalWrite(leftMotor1, LOW);
    digitalWrite(leftMotor2, LOW);
    digitalWrite(rightMotor1, LOW);
    digitalWrite(rightMotor2, LOW);
    delay(2);
  }
}
void fren() {
  digitalWrite(rightMotor1, HIGH);
  digitalWrite(rightMotor2, HIGH);


  digitalWrite(leftMotor1, HIGH);
  digitalWrite(leftMotor2, HIGH);
}
void wait() {
  digitalWrite(rightMotor1, LOW);
  digitalWrite(rightMotor2, LOW);


  digitalWrite(leftMotor1, LOW);
  digitalWrite(leftMotor2, LOW);
}
