import multiprocessing
import sys

import lifecycle
from CrossCuttingConcerns import mqtt_adapter, raspi_log
from Helpers import setup_helper
from Processes import readingQR_v3


def main():
    global process_life_cycle, process_qr
    client = mqtt_adapter.connect("START")
    startTopic = "start"

    process_setup = multiprocessing.Process(target=setup_helper.setup_ip)
    process_life_cycle = multiprocessing.Process(target=lifecycle.main)
    process_qr = multiprocessing.Process(target=readingQR_v3.main)

    # process_heartbeat = multiprocessing.Process(target=heartbeat.send_heartbeat)
    # process_obstacle = multiprocessing.Process(target=obstacle_detection.main)
    # process_web_server = multiprocessing.Process(target=WebServer.webServer.run)

    process_setup.start()  # setup ip for connecting access point
    process_setup.join()

    mqtt_adapter.subscribe(client, startTopic, callback_for_main_process)
    mqtt_adapter.loop_forever(client)


# process_heartbeat.start()
# process_obstacle.start()


# try:
#
# except Exception as e:
#     raspi_log.log_process(e)
# try:
#
# except Exception as e:
#     raspi_log.log_process(e)
#
# try:
#
# except Exception as e:
#     raspi_log.log_process(e)
# try:
#
# except Exception as e:
#     raspi_log.log_process(e)


# while (!allProcessesReady)
# empty

# above loop keep the process busy until all processes ready


# process_heartbeat.join()

def callback_for_main_process(client, userdata, msg):
    message = msg.payload.decode('utf-8')

    if message == "START":
        raspi_log.log_process("START REQUESTED processes are starting..")
        try:
            process_life_cycle.start()
            process_qr.start()
        except Exception as e:
            raspi_log.log_process(f"Error accured while starting application: {e}")

        raspi_log.log_process("Procceses which are succesfull started")
        # sendReadyMessage()

    if message == "STOP":
        raspi_log.log_process("STOP REQUESTED processes are stoping...")
        try:
            process_life_cycle.kill()
            process_qr.kill()
        except Exception as e:
            raspi_log.log_process(f"Error accured while stopping application: {e}")

        raspi_log.log_process("Procceses which are succesfull started")
        sys.exit()

    # process_qr.join()
    # process_life_cycle.join()


if __name__ == '__main__':
    main()
