import heartbeat
import lifecycle
from Helpers import configure_ip
import multiprocessing
from Sensors import obstacle_detection, readingQR_second#,readingQR


def main():
    process_setup_ip = multiprocessing.Process(target=configure_ip.setup_ip())
    process_life_cycle = multiprocessing.Process(target=lifecycle.main)

    process_qr = multiprocessing.Process(target=readingQR_second.main)
    process_heartbit = multiprocessing.Process(target=heartbeat.send_heartbeat)
    process_obstacle = multiprocessing.Process(target=obstacle_detection.main)

    process_setup_ip.start()  # setup ip for connecting access point
    process_setup_ip.join()
    process_life_cycle.start()
    process_heartbit.start()
    # process_obstacle.start()
    process_qr.start()



    process_qr.join()
    process_heartbit.join()
    process_life_cycle.join()



if __name__ == '__main__':
    main()
