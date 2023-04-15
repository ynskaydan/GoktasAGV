import cv2
import datetime
import os

from CrossCuttingConcerns import raspi_log, mqtt_adapter

topic = "qr"
time_old = datetime.datetime.now()


def main():
    raspi_log.log_process(str(f"Qr started! parent id:, {os.getppid()},  self id:, {os.getpid()}"))
    mqtt_adapter.connect("qr")
    old_data = ""

    # set up camera objects
    cap = cv2.VideoCapture(0)
    # QR code detection object
    detector = cv2.QRCodeDetector()

    while True:
        # get the image
        _, img = cap.read()
        # get bounding box coords and data
        data, bbox, _ = detector.detectAndDecode(img)

        # if there is a bounding box, draw one, along with the data
        if bbox is not None:
            #   for i in range(len(bbox)):
            #      cv2.line(img, tuple(bbox[i][0]), tuple(bbox[(i+1) % len(bbox)][0]), color=(255,
            #              0, 255), thickness=2)
            # cv2.putText(img, data, (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10), cv2.FONT_HERSHEY_SIMPLEX,
            #          0.5, (0, 255, 0), 2)
            if data:
                send_qr(data, old_data)
                old_data = data

        # display the image preview
        # cv2.imshow("code detector", img)
        if cv2.waitKey(1) == ord("q"):
            break
    # free camera object and exit
    cap.release()
    cv2.destroyAllWindows()
    mqtt_adapter.loop()


def send_qr(message, old_message):
    global topic, time_old
    global time_old
    time_now = datetime.datetime.now().second
    result = message
    if old_message != message:
        mqtt_adapter.publish(result, topic)
        raspi_log.log_process(result)
        time_old = time_now
    else:
        if (time_now - time_old) % 60 >= 10:
            mqtt_adapter.publish(result, topic)
            time_old = time_now
