from paho.mqtt import client as mqtt_client
import random


broker = "localhost"
port = 1883
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'goktas'
password = '12345678'


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect ", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def send_data(client, resultx, topic):
    result = client.publish(topic, resultx)
    status = result[0]
    if status == 0:
        print(f"Send '{resultx}' to topic '{topic}'")
    else:
        print(f"Failed to send message to topic {topic}")
