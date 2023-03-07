import paho.mqtt.client as mqtt


def mqtt_sub(broker, topic, on_message):
    print("saaa")

    def on_connect(client, userdata, flags, rc):
        print("Connected to MQTT broker.")
        client.subscribe(topic)



    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    print("Connecting..")
    client.connect(broker, 1883, 60)
    print("Connected")
    client.loop_forever()








# import datetime
#
# from paho.mqtt import client as mqtt_client
# from mqtt import connect_mqtt, sendData
#
#
# def subscribe(client: mqtt_client,topic):
#     def on_message(client, userdata, msg):
#         print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic on time '{datetime.datetime.now().minute}' '{datetime.datetime.now().second}'")
#         return msg
#
#     client.subscribe(topic)
#     client.on_message = on_message
#     return on_message()
#
#
#
#
# def sub_run(topic):
#     client = connect_mqtt()
#     subscribe(client,topic)
#     client.loop_forever()
#
#
#
#
