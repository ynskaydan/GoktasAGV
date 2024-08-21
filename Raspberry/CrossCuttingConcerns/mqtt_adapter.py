import datetime
import os

import paho.mqtt.client as mqtt_client

from constants import Constants

pub_topic = "raspi-log"
dir_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(os.path.dirname(dir_path), 'Database', 'db_logs.txt')
try:
    db_logs = open(file_path, "a")
except FileNotFoundError:
    db_logs = open(file_path, "w")


def connect(cid):
    global clientx
    client_id = f'mqtt-raspberry-{cid}'
    clientx = mqtt_client.Client()
    if Constants.develop_mode == True:
        broker = "localhost"
    else:
        broker = Constants.ip_addr
        clientx.username_pw_set(Constants.mqtt_username, Constants.mqtt_password)

    port = 1883

    def on_connect(client, userdata, flags, rc):
        now = datetime.datetime.now()
        if rc == 0:
            result = str(f"{now.hour}:{now.minute}:{now.second} Connected to MQTT Broker by  {cid}")
            log(result)
            return True
        else:
            result = str(f"{now.hour}:{now.minute}:{now.second} Failed to connect  {rc}")
            log(result)
            return False

    clientx.on_connect = on_connect
    clientx.connect(broker, port)
    return clientx


def publish(message, topic):
    now = datetime.datetime.now()
    result = clientx.publish(topic, message)
    status = result[0]
    if status == 0:
        resultx = str(
            f"{now.hour}:{now.minute}:{now.second} Message '{message}' sent to topic '{topic}'")

    else:
        resultx = str(
            f"{now.hour}:{now.minute}:{now.second} Failed to send message to topic {topic}")

    print(resultx)
    db_logs.write(resultx)


def subscribe(client, topic, callback):
    now = datetime.datetime.now()
    client.subscribe(topic)
    client.message_callback_add(topic, callback)
    result = str(f"{now.hour}:{now.minute}:{now.second} Subscribed to {topic}")
    log(result)


def loop_forever(client):
    client.loop_forever()


def loop():
    clientx.loop()


def log(message):
    print(message)
    publish(message, pub_topic)
    db_logs.write(str("\n" + message))
