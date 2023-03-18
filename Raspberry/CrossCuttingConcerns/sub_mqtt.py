import paho.mqtt.client as mqtt


def mqtt_sub(broker, topics, on_message_methods):
    client = mqtt.Client()

    def on_connect(client, userdata, flags, rc):
        print(f"Connected to MQTT broker with subscription of")
        for topic in topics:
            print(f"{topic},")

    client.connect(broker, 1883, 60)
    client.on_connect = on_connect
    for i in range(0,len(topics)):
        client.subscribe(topics[i])
        client.message_callback_add(topics[i],on_message_methods[i])

    client.loop_forever()
