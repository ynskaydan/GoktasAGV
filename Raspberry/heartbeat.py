import os
import time
import os

from CrossCuttingConcerns import mqtt_adapter


def send_heartbeat():
    print("Heartbeat başladı!")
    print("Heartbeat started! parent id:", os.getppid(), " self id:", os.getpid())
    topic = "heartbeat"
    message = "heartbeat"
    mqtt_adapter.connect("hb")
    while True:
        mqtt_adapter.loop()
        mqtt_adapter.publish(message,topic)
        time.sleep(5)  # 5 saniye bekleme
