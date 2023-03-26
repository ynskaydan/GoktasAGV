#include <UIPEthernet.h>
#include <PubSubClient.h>
#include <L298NX2.h>

// Ethernet modülü pinleri
#define SCK_PIN 13
#define MISO_PIN 12
#define MOSI_PIN 11
#define SS_PIN 10

// Ethernet bağlantısı için kullanılan MAC adresi ve IP adresi
byte mac[] = {0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED};
IPAddress ip(192, 168, 1, 177);

// MQTT broker adresi ve bağlantı bilgileri
const char* mqtt_server = "broker.hivemq.com";
const char* client_id = "arduino-client";
const char* heartbeat_topic = "heartbeat";

EthernetClient ethClient;
PubSubClient mqttClient(ethClient);

// Motor sürücü pinleri
const unsigned int EN_left = 5;
const unsigned int leftmotor1 = 8;
const unsigned int leftmotor2 = 9;

const unsigned int rightmotor1 = 10;
const unsigned int rightmotor2 = 11;
const unsigned int EN_right = 6;

L298NX2 motors(EN_right, rightmotor1, rightmotor2, EN_left, leftmotor1, leftmotor2);


// Zamanlayıcı değişkenleri
unsigned long last_heartbeat = 0;
const unsigned long heartbeat_interval = 500;

void setup() {
  // Motor sürücü pinleri için çıkış modu ayarlanır
  
  // Ethernet modülü başlatılır ve IP adresi atanır
  Ethernet.begin(mac, ip);
  
  // MQTT client başlatılır ve broker'a bağlanılır
  mqttClient.setServer(mqtt_server, 1883);
  mqttClient.setCallback(callback);
  connectToMQTTBroker();
}

void loop() {
  mqttClient.loop();
  if (millis() - last_heartbeat > heartbeat_interval) {
    motors.stop();
    // Motorları durdurur
  }
}
void connectToMQTTBroker() {
  while (!mqttClient.connected()) {
    Serial.println("MQTT broker'a bağlanılıyor...");
    if (mqttClient.connect(client_id)) {
      Serial.println("MQTT broker'a bağlanıldı.");
      mqttClient.subscribe(heartbeat_topic);
    } else {
      Serial.print("Bağlantı hatası: ");
      Serial.println(mqttClient.state());
      delay(5000);
    }
  }
}

// "heartbeat" konusu dinlendiğinde çağırılan fonksiyon
void callback(char* topic, byte* payload, unsigned int length) {
  String message;
  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }
  
  // Eğer "heartbeat" mesajı geldiyse zamanlayıcıyı sıfırla
  if (message == "heartbeat") {
    last_heartbeat = millis();
  }
}


