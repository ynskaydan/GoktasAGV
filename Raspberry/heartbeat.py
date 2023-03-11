from mqtt import connect_mqtt, sendData

topic = "hearbeat"
client = connect_mqtt()
def send_heartbeat():
    
    while True:
        send_data(client, "heartbeat", heartbeat_topic)
        time.sleep(5)  # 5 saniye beklemeP