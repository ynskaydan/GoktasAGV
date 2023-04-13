import heartbeat
import lifecycle
from CrossCuttingConcerns import mqtt_adapter
from Helpers import ip_helper
import multiprocessing
from Sensors import obstacle_detection, readingQR  # ,readingQR


def main():
    process_setup_ip = multiprocessing.Process(target=ip_helper.setup_ip)
    process_life_cycle = multiprocessing.Process(target=lifecycle.main)

    process_qr = multiprocessing.Process(target=readingQR.main)
    process_heartbit = multiprocessing.Process(target=heartbeat.send_heartbeat)
    # process_obstacle = multiprocessing.Process(target=obstacle_detection.main)

    process_setup_ip.start()  # setup ip for connecting access point
    process_setup_ip.join()

    process_heartbit.start()
    # process_obstacle.start()
    process_qr.start()
    process_life_cycle.start()

    # while (!allProcessesReady)
    # empty

    # above loop keep the process busy until all processes ready

    # sendReadyMessage()

    process_qr.join()
    process_heartbit.join()
    process_life_cycle.join()


if __name__ == '__main__':
    main()

