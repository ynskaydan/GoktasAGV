import datetime
import os

from paho.mqtt import client as mqtt_client

pub_topic = "raspi-log"
dir_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(os.path.dirname(dir_path), 'Database', 'db_logs.txt')
try:
    db_logs = open(file_path,"a")
except FileNotFoundError:
    db_logs = open(file_path, "w")


def connect(cid):
    global client

    broker = "10.32.16.208"
    port = 1883
    client_id = f'mqtt-raspberry-{cid}'
    username = "goktas"
    password = "12345678"

    client = mqtt_client.Client()
    client.username_pw_set(username, password)

    def on_connect(client, userdata, flags, rc):
        now = datetime.datetime.now()
        if rc == 0:
            result = str(f"{now.hour}:{now.minute}:{now.second} Connected to MQTT Broker by  {client_id}")
            log(result)
            return True
        else:
            result = str(f"{now.hour}:{now.minute}:{now.second} Failed to connect  {rc}")
            log(result)
            return False

    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client,message, topic):
    now = datetime.datetime.now()
    result = client.publish(topic, message)
    status = result[0]
    if status == 0:
        resultx = str(
            f"{now.hour}:{now.minute}:{now.second} Message '{message}' sent to topic '{topic}'")

    else:
        resultx = str(
            f"{now.hour}:{now.minute}:{now.second} Failed to send message to topic {topic}")

    print(resultx)
    db_logs.write(resultx)


def subscribe(client,topic, callback):

    now = datetime.datetime.now()
    client.subscribe(topic)
    client.message_callback_add(topic, callback)
    result = str(f"{now.hour}:{now.minute}:{now.second} Subscribed to {topic}")
    log(result)


def loop_forever():
    client.loop_forever()


def loop():
    client.loop()


def log(message):
    print(message)
    publish(client,message, pub_topic)
    db_logs.write(str("\n" + message))
