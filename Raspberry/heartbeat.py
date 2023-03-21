import time
from CrossCuttingConcerns.mqtt import connect_mqtt, send_data


def send_heartbeat():
    print("Heartbeat başladı!")
    topic = "heartbeat"
    client = connect_mqtt()
    while True:
        send_data(client, "heartbeat", topic)
        time.sleep(5)  # 5 saniye bekleme
