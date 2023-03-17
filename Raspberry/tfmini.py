# -*- coding: utf-8 -*
import serial
import time

from CrossCuttingConcerns.mqtt import send_data, connect_mqtt

ser = serial.Serial("/dev/ttyS0", 115200)

client = connect_mqtt()
topic = "obstacle_detection"


def get_lidar_data():
    while True:

        count = ser.in_waiting
        if count > 8:
            recv = ser.read(9)
            ser.reset_input_buffer()
            if recv[0] == 0x59 and recv[1] == 0x59:  # 0x59 is 'Y'
                distance = recv[2] + recv[3] * 256
                strength = recv[4] + recv[5] * 256
                print('(', distance, ',', strength, ')')
                send_data(client, distance, topic)
                time.sleep(1)


if __name__ == '__main__':
    try:
        if ser.is_open == False:
            ser.open()
        get_lidar_data()
    except KeyboardInterrupt:  # Ctrl+C
        if ser != None:
            ser.close()
