import os
import time
import os

from CrossCuttingConcerns import mqtt_adapter, raspi_log


def send_heartbeat():

    raspi_log.log_process(str(f"Heartbeat started! parent id: {os.getppid()},  self id: {os.getpid()}"))
    topic = "heartbeat"
    message = "heartbeat"
    mqtt_adapter.connect("heartbeat")
    while True:
        mqtt_adapter.publish(message,topic)
        time.sleep(5)  # 5 saniye bekleme
        mqtt_adapter.loop()
