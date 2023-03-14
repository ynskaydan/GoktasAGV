import cv2
import datetime
from CrossCuttingConcerns.mqtt import connect_mqtt, send_data

topic = "qr"

time_old = datetime.datetime.now();


def publish(client, message, oldmessage):
    global time_old
    time_now = datetime.datetime.now()
    resultx = message + " on time: " + \
              str(datetime.datetime.now().minute) + ":" + \
              str(datetime.datetime.now().second)
    if (oldmessage != message):
        send_data(client, resultx)
        time_old = time_now
    else:
        if ((time_now.second - time_old.second) % 60 >= 10):
            send_data(client, resultx)
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
    # cv2.imshow("code detector", img)
    if (cv2.waitKey(1) == ord("q")):
        break
# free camera object and exit
cap.release()
cv2.destroyAllWindows()
