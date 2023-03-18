#include <EthernetENC.h>
#include <PubSubClient.h>
#include <L298NX2.h>
#include <QTRSensors.h>

#define Kp 0.4
#define Kd 2.2
#define rightMaxSpeed 80
#define leftMaxSpeed 80
#define rightBaseSpeed 65
#define leftBaseSpeed 65

#define leftFarSensor 49
#define leftOuterSensor 48
#define leftNearSensor 47
#define leftNearSensor2 46
#define leftNearSensor3 45
#define leftNearSensor4 44
#define leftNearSensor5 43
#define leftCenterSensor 42
#define rightCenterSensor 41
#define rightNearSensor5 40
#define rightNearSensor4 39
#define rightNearSensor3 38
#define rightNearSensor2 37
#define rightNearSensor 36
#define rightOuterSensor 35
#define rightFarSensor 34

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

// MQTT sunucu bilgileri
const char* mqtt_server = "192.168.1.100";
const int mqtt_port = 1883;

// ENC28J60 ethernet modülü ayarları
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
byte ip[] = { 192, 168, 1, 43 };
byte subnet[] = { 255, 255, 255, 0 };
byte gateway[] = { 192, 168, 1, 1 };

// MQTT konusu ve istemci adı
const char* mqtt_topic_move = "move";
const char* mqtt_topic_heartbit = "heartbit";
const char* mqtt_client_name = "arduino";

// MQTT istemci nesnesi
EthernetClient ethClient;
PubSubClient mqttClient(ethClient);
void setup() {
  Serial.begin(9600);

  // ENC28J60 ethernet modülünü başlat
  Ethernet.init(10);
  Ethernet.begin(mac, ip, gateway, subnet);
  while (Ethernet.linkStatus() == LinkOFF) {
    Serial.println("Ethernet cable is not connected");
    delay(500);
  }
  Serial.println("Ethernet connected");
  // MQTT istemcisini ayarla
  mqttClient.setServer(mqtt_server, mqtt_port);
  mqttClient.setCallback(callback);

  while (!mqttClient.connected()) {
    if (mqttClient.connect("Arduino client")) {
      Serial.println("Connected to MQTT broker");
      mqttClient.subscribe(mqtt_topic_move);
      mqttClient.subscribe(mqtt_topic_heartbit);
    } else {
      Serial.print("Failed to connect to MQTT broker, rc=");
      Serial.print(mqttClient.state());
      Serial.println(" retrying...");
      delay(5000);
    }
  }

  qtr.setTypeRC();
  qtr.setSensorPins((const uint8_t[]){ 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49 }, SensorCount);
  qtr.setEmitterPin(2);
  pinMode(rightMotor1, OUTPUT);
  pinMode(rightMotor2, OUTPUT);
  pinMode(rightMotorE, OUTPUT);
  pinMode(leftMotor1, OUTPUT);
  pinMode(leftMotor2, OUTPUT);
  pinMode(leftMotorE, OUTPUT);


  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);  // turn on Arduino's LED to indicate we are in calibration mode


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

  delay(1000);
}

void loop() {
  // MQTT bağlantısını kontrol et
  if (!mqttClient.connected()) {
    reconnect();
  }
  mqttClient.loop();
}

void reconnect() {
  while (!mqttClient.connected()) {
    Serial.println("Attempting MQTT connection...");
    if (mqttClient.connect("ArduinoClient")) {
      Serial.println("Connected to MQTT broker");
      mqttClient.subscribe(mqtt_topic_move);
      mqttClient.subscribe(mqtt_topic_heartbit);
    } else {
      Serial.print("Failed to connect to MQTT broker, rc=");
      Serial.print(mqttClient.state());
      Serial.println(" retrying...");
      delay(5000);
    }
  }
}
QTRSensors qtr;

const uint8_t SensorCount = 16;
unsigned int sensorValues[SensorCount];
const unsigned int EN_left = 10;
const unsigned int leftmotor1 = 4;
const unsigned int leftmotor2 = 5;

const unsigned int rightmotor1 = 2;
const unsigned int rightmotor2 = 3;
const unsigned int EN_right = 9;

L298NX2 motors(EN_right, rightmotor1, rightmotor2, EN_left, leftmotor1, leftmotor2);


void callback(char* topic, byte* message, unsigned int length) {
  String topicStr = String(topic);
  String messageStr = "";

  for (int i = 0; i < length; i++) {
    messageStr += (char)message[i];
  }

  if (topicStr == mqtt_topic_move) {
    // callback for topic1
    manualControl(messageStr);
    Serial.println("Received message on topic1: " + messageStr);
    // do something
  } else if (topicStr == mqtt_topic_heartbit) {

    Serial.println("Received message on topic2: " + messageStr);
  } else if (topicStr == "eklenecek topic") {
  }
}


void manualControl(String message) {

  if (message == "W") {
    Serial.println("Ileri mesaji alindi");
    motors.run(L298N::FORWARD);
    motors.setSpeedB(60);
    motors.setSpeedA(60);
  } else if (message == "S") {
    Serial.println("Geri mesaji alindi");
    motors.run(L298N::BACKWARD);
    motors.setSpeedB(60);
    motors.setSpeedA(60);
  } else if (message == "D") {
    Serial.println("Sag mesaji alindi");
    motors.run(L298N::FORWARD);
    motors.setSpeedB(0);
    motors.setSpeedA(60);
  } else if (message == "A") {
    Serial.println("Sol mesaji alindi");
    motors.run(L298N::FORWARD);
    motors.setSpeedB(60);
    motors.setSpeedA(0);
  }
}


void loopLineFollowing() {
  int lastError = 0;
  // read calibrated sensor values and obtain a measure of the line position
  unsigned int position = qtr.readLineBlack(sensorValues);


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
