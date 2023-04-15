# -*- coding: utf-8
import os

from serial import Serial

from CrossCuttingConcerns import mqtt_adapter, raspi_log

topic = "obstacle_detection"
stop_distance = 100


def main():
    raspi_log.log_process(str(f"Obstacle detection started! parent id:, {os.getppid()},  self id:, {os.getpid()}"))

    ser = Serial("/dev/ttyS0", 115200)
    mqtt_adapter.connect("obstacle")

    try:
        if not ser.is_open:
            ser.open()

        get_lidar_data(ser)

    except KeyboardInterrupt:  # Ctrl+C
        if ser is not None:
            ser.close()


def get_lidar_data(ser):
    while True:
        count = ser.in_waiting
        if count > 8:
            recv = ser.read(9)
            ser.reset_input_buffer()
            if recv[0] == 0x59 and recv[1] == 0x59:  # 0x59 is 'Y'
                distance = recv[2] + recv[3] * 256
                strength = recv[4] + recv[5] * 256
                if distance < stop_distance:
                    result = f"obstacle detected! {distance}"
                    raspi_log.log_process(result)
                    mqtt_adapter.publish(result, topic)
