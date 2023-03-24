import heartbeat
import os
import mapping
import time
from CrossCuttingConcerns.mqtt import connect_mqtt, broker
from CrossCuttingConcerns.sub_mqtt import mqtt_sub

import multiprocessing

from Sensors import readingQR, obstacle_detection

sub_mode_topic = "mode"
sub_topics = [sub_mode_topic]
mode = ""

<<<<<<< HEAD

heartbeat_thread = threading.Thread(heartbeat.send_heartbeat())
qr_thread = threading.Thread(readingQR.main()) # Collecting all functions to thread
mapping_thread = threading.Thread(mapping.main())
obstacle_thread = threading.Thread(obstacle_detection.main())

qr_thread.start() # Starting global threads
qr_thread.join()
heartbeat_thread.start()
heartbeat_thread.join()
obstacle_thread.start()
obstacle_thread.join()


 # Waiting to stop threads


=======
>>>>>>> main

def callback_for_mode(client, userdata, msg):
    global mode
    message = msg.payload.decode('utf-8')
    mode_functions = {
        "explore": run_explore_mode,
        "import": run_import_mode,
        "export": run_export_mode,
        "duty": run_duty_mode,
    }
    if message in mode_functions:
        mode = message
        mode_functions[message]()





def run_explore_mode():
    print("Mapping active")
    try:
<<<<<<< HEAD
        mapping_thread.start()
        mapping_thread.join()
    except:
        print("mapping is stopped")
=======
        process_mapping.start()
    except AssertionError:
        print("Cannot start a process twitce")

def run_duty_mode():
    print("Duty active")
    process_mapping.terminate()

>>>>>>> main


def run_import_mode():
    try:
        print("importing")
    except AssertionError:
        print("Cannot start a process twitce")


def run_export_mode():
    try:
        print("exporting")
    except AssertionError:
        print("Cannot start a process twitce")


on_message_methods = [callback_for_mode]


def main():
    global on_message_methods
    global process_mapping
    process_qr = multiprocessing.Process(target=readingQR.main)
    process_heartbit = multiprocessing.Process(target=heartbeat.send_heartbeat)
    process_mapping = multiprocessing.Process(target=mapping.main)
    process_obstacle = multiprocessing.Process(target=obstacle_detection.main)
    process_heartbit.start()
    # process_obstacle.start()
    process_qr.start()

    print("ID of process heartbit: {}".format(process_heartbit.pid))
    print("ID of process qr: {}".format(process_qr.pid))

    client = connect_mqtt()

    mqtt_sub(broker, sub_topics, on_message_methods)
    process_qr.join()
    process_heartbit.join()


if __name__ == '__main__':
    main()
