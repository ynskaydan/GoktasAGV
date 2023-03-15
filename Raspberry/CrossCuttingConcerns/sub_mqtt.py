import paho.mqtt.client as mqtt


def mqtt_sub(broker, topic, on_message_topic1, topic2, on_message_topic2):
    client = mqtt.Client()

    def on_connect(client, userdata, flags, rc):
        print(f"Connected to MQTT broker with subscription of {topic} and {topic2}.")

    client.connect(broker, 1883, 60)
    client.on_connect = on_connect

    client.subscribe(topic)
    client.message_callback_add(topic, on_message_topic1)
    client.subscribe(topic2)
    client.message_callback_add(topic2, on_message_topic2)

    client.loop_forever()
