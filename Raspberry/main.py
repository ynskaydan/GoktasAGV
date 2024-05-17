
from Processes import readingQR
#import lifecycle
#from CrossCuttingConcerns import mqtt_adapter
#from Helpers import setup_helper
import multiprocessing
#from Sensors import obstacle_detection


def main():
    #process_setup = multiprocessing.Process(target=setup_helper.setup_ip)
   # process_life_cycle = multiprocessing.Process(target=lifecycle.main)
    process_qr = multiprocessing.Process(target=readingQR.main)
    #process_heartbeat = multiprocessing.Process(target=heartbeat.send_heartbeat)
    #process_obstacle = multiprocessing.Process(target=obstacle_detection.main)

    #process_setup.start()  # setup ip for connecting access point
    #process_setup.join()
    process_qr.start()
    #process_heartbeat.start()
    #process_obstacle.start()
   # process_life_cycle.start()


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

    # sendReadyMessage()

    process_qr.join()
    #process_heartbeat.join()
   # process_life_cycle.join()


if __name__ == '__main__':
    main()
