import os
import time
from CrossCuttingConcerns.mqtt import connect_mqtt, send_data
import os


def send_heartbeat():
    print("Heartbeat başladı!")
    print("Heartbeat started! parent id:", os.getppid(), " self id:", os.getpid())
    topic = "heartbeat"
    client = connect_mqtt()
    while True:
        send_data(client, "heartbeat", topic)
        time.sleep(5)  # 5 saniye bekleme
