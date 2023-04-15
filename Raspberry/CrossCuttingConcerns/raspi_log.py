import datetime
import os

from CrossCuttingConcerns import mqtt_adapter

mqtt_adapter.connect("log")
dir_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(os.path.dirname(dir_path), 'Database', 'db_logs.txt')
db_logs = open(file_path, "a")
pub_topic = "raspi-log"

<<<<<<< HEAD
=======

>>>>>>> main
def log_process(message):
    now = datetime.datetime.now()
    result = str(f"{now.hour}:{now.minute}:{now.second} {message}")
    print(result)
    mqtt_adapter.publish(result, pub_topic)
    db_logs.write(str("\n" + result))
