#include <QTRSensors.h>

#define Kp 0.4 
#define Kd 2.2 
#define rightMaxSpeed 75 
#define leftMaxSpeed 75
#define rightBaseSpeed 65 
#define leftBaseSpeed 65 

#define leftFarSensor 34
#define leftOuterSensor 35
#define leftNearSensor 36
#define leftNearSensor2 37
#define leftNearSensor3 38
#define leftNearSensor4 39
#define leftNearSensor5 40
#define leftCenterSensor 41
#define rightCenterSensor 42
#define rightNearSensor5 43
#define rightNearSensor4 44
#define rightNearSensor3 45
#define rightNearSensor2 46
#define rightNearSensor 47
#define rightOuterSensor 48
#define rightFarSensor 49
int leftCenterReading;
int leftNearReading;
int leftOuterReading;
int leftFarReading;
int rightCenterReading;
int rightNearReading;
int rightOuterReading;
int rightFarReading;

#define leapTime 450
#define leftMotor1 4
#define leftMotor2 5
#define rightMotor1 2
#define rightMotor2 3
#define leftMotorE 10
#define rightMotorE 9

#define led 13

int leftspeed;
int rightspeed;
int donushizi=90;

QTRSensors qtr;

const uint8_t SensorCount = 16;
unsigned int sensorValues[SensorCount];
unsigned int posit;

void setup() {
   qtr.setTypeRC();
   qtr.setSensorPins((const uint8_t[]){34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49}, SensorCount);
 
  pinMode(leftCenterSensor, INPUT);
  pinMode(leftNearSensor, INPUT);
  pinMode(leftNearSensor2, INPUT);
  pinMode(leftNearSensor3, INPUT);
  pinMode(leftNearSensor4, INPUT);
  pinMode(leftNearSensor5, INPUT);
  pinMode(leftOuterSensor, INPUT);
  pinMode(leftFarSensor, INPUT);
  pinMode(rightCenterSensor, INPUT);
  pinMode(rightNearSensor, INPUT);
  pinMode(rightNearSensor2, INPUT);
  pinMode(rightNearSensor3, INPUT);
  pinMode(rightNearSensor4, INPUT);
  pinMode(rightNearSensor5, INPUT);
  pinMode(rightOuterSensor, INPUT);
  pinMode(rightFarSensor, INPUT);
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

  delay(3000); 
}
  void loop() {
  readSensors();
  while ((leftFarReading < 200 && rightFarReading < 200 ) && (leftCenterReading > 200 && rightCenterReading > 200 )) {
    delay(1500);
    ilerle();
    delay(6);
    Serial.println("ilerliyor");
    readSensors();
   }

  
    crossroadFinding();
  
}
void readSensors() {
  leftCenterReading = digitalRead(leftCenterSensor);
  leftNearReading = digitalRead(leftNearSensor);
  leftOuterReading = digitalRead(leftOuterSensor);
  leftFarReading = digitalRead(leftFarSensor);
  rightCenterReading = digitalRead(rightCenterSensor);
  rightNearReading = digitalRead(rightNearSensor);
  rightOuterReading = digitalRead(rightOuterSensor);
  rightFarReading = digitalRead(rightFarSensor);
}
void crossroadFinding() {
 /*if (leftFarReading < 200 && rightFarReading < 200 && leftOuterReading < 200 && rightOuterReading < 200 && leftNearReading < 200 && rightNearReading < 200 && leftCenterReading < 200 && rightCenterReading < 200) {
    turnAround();
    Serial.println("geri dönüyor");
    return;
  }*/
    if ((leftNearReading > 200 && rightNearReading > 200) || (leftOuterReading > 200 && rightOuterReading > 200) ) {
      Serial.println("T kavşak algılandı");
      digitalWrite(leftMotor1,HIGH);
      digitalWrite(leftMotor2, LOW);
      digitalWrite(rightMotor1, HIGH);
      digitalWrite(rightMotor2, LOW);
      analogWrite(rightMotorE, rightBaseSpeed);
      analogWrite(leftMotorE, leftBaseSpeed);
      delay(leapTime);
       // çizgiyi geçtikten sonra tekrar sensör değeri okuyor
      readSensors();
     
      // sağ ve solda çizgi yoksa planlandığı halindeyken input gelmesini bekleyecek
      if (leftFarReading < 200 && rightFarReading < 200) {
        Serial.println("Sola dönülüyor...");
        delay(1500);
        turnLeft();
      }
    return;
    }
  if (leftFarReading > 200 && rightFarReading < 200) { 
    Serial.println("Sol L kavşak algılandı.");
    digitalWrite(leftMotor1,HIGH);
    digitalWrite(leftMotor2, LOW);
    digitalWrite(rightMotor1, HIGH);
    digitalWrite(rightMotor2, LOW);
  analogWrite(rightMotorE, rightBaseSpeed);
  analogWrite(leftMotorE, leftBaseSpeed);
    delay(leapTime);
    readSensors();
    if (leftFarReading < 200 && leftOuterReading < 200) { 
      Serial.println("Sola dönülüyor");
      delay(1500);
      turnLeft();
    }
   
    return;

  }
  if ((rightFarReading > 200 && rightOuterReading > 200) && (leftFarReading < 200 && leftOuterReading < 200)) { // sağa dönüş
    Serial.println("Sağ L kavşak algılandı.");
    digitalWrite(leftMotor1,HIGH);
    digitalWrite(leftMotor2, LOW);
    digitalWrite(rightMotor1, HIGH);
    digitalWrite(rightMotor2, LOW);
  analogWrite(rightMotorE, rightBaseSpeed);
  analogWrite(leftMotorE, leftBaseSpeed);
    delay(leapTime);
    readSensors();
    if (leftCenterReading > 200 || rightCenterReading > 200) { 
      Serial.println("ortadan gidiyor");
      delay(1500);
      ilerle();
      return;
    }
    else  { 
    delay(1500);    
      turnRight();
      Serial.println("Sağa dönüş yapılıyor...");
      return;
    }

  }
}

void turn_left() {
      digitalWrite(rightMotor1,HIGH);
    digitalWrite(rightMotor2, LOW);
    analogWrite (rightMotorE,90); 

    digitalWrite(leftMotor1, LOW);
    digitalWrite(leftMotor2, HIGH);
    analogWrite (leftMotorE,90);
}
void turn_right() {
      digitalWrite(rightMotor1,LOW);
    digitalWrite(rightMotor2, HIGH);
    analogWrite (rightMotorE,90);   

    digitalWrite(leftMotor1, HIGH);
    digitalWrite(leftMotor2, LOW);
    analogWrite (leftMotorE,90);    
}
void turnLeft() {
  
    
  while (digitalRead(leftCenterSensor) > 200 || digitalRead(rightCenterSensor) > 200 ) {
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
  while (digitalRead(leftCenterSensor) < 200) {
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
  while (digitalRead(rightCenterSensor) < 200) {
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
  

}//voidturnleft
void turnRight() {
    
  while (digitalRead(leftCenterSensor) > 200 || digitalRead(rightCenterSensor) > 200 ) {
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
 
  while (digitalRead(rightCenterSensor) < 200) {
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
  while (digitalRead(leftCenterSensor) < 200) {
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
} //voidturnright
void ilerle()
{
  unsigned int position = qtr.readLineBlack(sensorValues);

  int lastError = 0;
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


void turnAround() {
  digitalWrite(leftMotor1,HIGH);
  digitalWrite(leftMotor2, LOW);
  digitalWrite(rightMotor1, HIGH);
  digitalWrite(rightMotor2, LOW);
  analogWrite(rightMotorE, rightBaseSpeed);
  analogWrite(leftMotorE, leftBaseSpeed);
  delay(leapTime);
  while (digitalRead(rightCenterSensor) < 200) {
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
    digitalWrite(rightMotor1,HIGH);
    digitalWrite(rightMotor2, HIGH);
   

    digitalWrite(leftMotor1, HIGH);
    digitalWrite(leftMotor2, HIGH);
    
}
void wait() {
    digitalWrite(rightMotor1,LOW);
    digitalWrite(rightMotor2, LOW);
   

    digitalWrite(leftMotor1, LOW);
    digitalWrite(leftMotor2, LOW);
    
}

