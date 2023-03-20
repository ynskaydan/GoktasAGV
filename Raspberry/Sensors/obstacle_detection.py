# -*- coding: utf-8 -*
import serial
import time
from CrossCuttingConcerns.mqtt import send_data, connect_mqtt


def main():
    #global ser, client, topic
    ser = serial.Serial("/dev/ttyS0", 115200)
    client = connect_mqtt()
    topic = "obstacle_detection"
    if __name__ == '__main__':
        try:
            if ser.is_open == False:
                ser.open()
            data = get_lidar_data(ser)
            print(f"distance: {data[0]}, strength: {data[1]}")
            send_data(client,data[0],topic)

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
                return distance,strength
