from paho.mqtt import client as mqtt_client
from mqtt import connect_mqtt, sendData

topic = "hb"
messageToSend = "connection approved"
def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        if(msg == "connection approved"):
            sendData(client,messageToSend,topic)

    client.subscribe(topic)
    client.on_message = on_message



def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()

