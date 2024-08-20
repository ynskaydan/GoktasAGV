# -*- coding: utf-8
import os
import time

from serial import Serial

from Services import arduino_manager
from CrossCuttingConcerns import mqtt_adapter, raspi_log

topic = "obstacle_detection"
stop_distance = 100

obstacle_state = False


def main():
    try:
        lidar_main()
    except Exception as e:
        raspi_log.log_process(f"There was faced with error on lidar: {e}")


def lidar_main():
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
    global obstacle_state
    while True:
        count = ser.in_waiting
        if count > 8:
            recv = ser.read(9)
            ser.reset_input_buffer()
            if recv[0] == 0x59 and recv[1] == 0x59:  # 0x59 is 'Y'
                distance = recv[2] + recv[3] * 256
                strength = recv[4] + recv[5] * 256
                if distance < stop_distance:
                    arduino_manager.stop_autonomous_motion_of_vehicle()
                    if not obstacle_state:
                        result = f"obstacle detected! {distance}"
                        raspi_log.log_process(result)
                        time.sleep(15)
                        if distance<stop_distance:
                            mqtt_adapter.publish(client,result, topic)
                            arduino_manager.start_obstacle_flow(distance)
                            set_obstacle_state(True)
                        else:
                            arduino_manager.start_autonomous_motion_of_vehicle()


def set_obstacle_state(bool):
    global obstacle_state
    obstacle_state = bool


def callback_for_end_obstacle():
    set_obstacle_state(False)
