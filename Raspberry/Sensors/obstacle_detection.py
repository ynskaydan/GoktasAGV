# -*- coding: utf-8 -*
import serial

from CrossCuttingConcerns import mqtt_adapter


def main():
    print("Engel Tespit Başladı!")
    stop_distance = 100
    ser = serial.Serial("/dev/ttyS0", 115200)
    mqtt_adapter.connect()
    topic = "obstacle_detection"
    try:
        if not ser.is_open:
            ser.open()

        data = get_lidar_data(ser)

        if data[0] < stop_distance:
            result = f"obstacle detected! {data[0]}"
            mqtt_adapter.publish(result,topic)

    except KeyboardInterrupt:  # Ctrl+C
        if ser != None:
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
                return distance, strength
