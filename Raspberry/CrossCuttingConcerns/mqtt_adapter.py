from paho.mqtt import client as mqtt_client


def connect(id):
    global client
    broker = "localhost"
    port = 1883
    client_id = f'mqtt-raspberry-{id}'
    username = 'goktas'
    password = '12345678'

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(f"Connected to MQTT Broker from client {client_id}")
            return True
        else:
            print("Failed to connect ", rc)
            return False

    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(message, topic):
    result = client.publish(topic, message)
    status = result[0]
    if status == 0:
        print(f"Message '{message}' sent to topic '{topic}' cid: {client.client_id}")
    else:
        print(f"Failed to send message to topic {topic} cid: {client.client_id}")


def subscribe(topic, callback):

    client.subscribe(topic)
    client.message_callback_add(topic, callback)
    print(f"Subscribed to {topic}")


def loop_forever():
    client.loop_forever()


def loop():
    client.loop()
