from CrossCuttingConcerns import mqtt_adapter, raspi_log
import os
direction = ""
sub_topic = "imu"  # imu manager hem speed hem direction
speed = ""


def main():
    raspi_log.log_process(str(f"Imu started! parent id: {os.getppid()},  self id: {os.getpid()}"))
    mqtt_adapter.connect("imu")
    mqtt_adapter.subscribe(sub_topic, callback)


def callback(client, userdata, msg):
    global direction, speed
    message = msg.payload.decode('utf-8')
    parts = message.split(";")
    direction = parts[0]
    speed = parts[1]


def get_direction():
    return direction


def get_speed():
    return speed
