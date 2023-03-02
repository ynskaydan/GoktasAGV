from tokenize import String
import cv2
from paho.mqtt import client as mqtt_client
import random
import time
import datetime
import paho.mqtt.client as paho

broker = "192.168.0.20"
port = 1883
topic = "qr"
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'goktas'
password = '12345678'


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("FAiled to connect ", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def sendData(client, resultx):
    result = client.publish(topic, resultx)
    status = result[0]
    if status == 0:
        print(f"Send '{resultx}' to topic '{topic}'")
    else:
        print(f"Failed to send message to topic {topic}")


time_old = datetime.datetime.now();


def publish(client, message, oldmessage):
    global time_old
    time_now = datetime.datetime.now()
    resultx = message + " on time: " + \
              str(datetime.datetime.now().minute) + ":" + \
              str(datetime.datetime.now().second)
    if (oldmessage != message):
        sendData(client, resultx)
        time_old = time_now
    else:
        if ((time_now.second - time_old.second) % 60 >= 10):
            sendData(client, resultx)
            time_old = time_now


client = connect_mqtt()

# set up camera objects
cap = cv2.VideoCapture(0)

# QR code detection object
detector = cv2.QRCodeDetector()
olddata = ""
while True:
    # get the image
    _, img = cap.read()
    # get bounding box coords and data
    data, bbox, _ = detector.detectAndDecode(img)

    # if there is a bounding box, draw one, along with the data
    if (bbox is not None):
        #   for i in range(len(bbox)):
        #      cv2.line(img, tuple(bbox[i][0]), tuple(bbox[(i+1) % len(bbox)][0]), color=(255,
        #              0, 255), thickness=2)
        # cv2.putText(img, data, (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10), cv2.FONT_HERSHEY_SIMPLEX,
        #          0.5, (0, 255, 0), 2)
        if data:
            print("data found: ", data)
            publish(client, data, olddata)
            olddata = data;

    # display the image preview
    #cv2.imshow("code detector", img)
    if (cv2.waitKey(1) == ord("q")):
        break
# free camera object and exit
cap.release()
cv2.destroyAllWindows()
