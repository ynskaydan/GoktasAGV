import cv2
from pyzbar.pyzbar import decode
import datetime
import os

from CrossCuttingConcerns import raspi_log, mqtt_adapter

topic = "qr"
time_old = datetime.datetime.now()


def main():
    try:
        read_qr()
    except Exception as e:
        raspi_log.log_process(f"There was faced with error on camera object: {e}")


def read_qr():
    raspi_log.log_process(f"Qr started! Parent ID: {os.getppid()}, Self ID: {os.getpid()}")
    mqtt_adapter.connect("qr")
    old_data = ""

    # Set up camera object
    cap = cv2.VideoCapture(0, cv2.CAP_V4L)

    while True:
        ret, img = cap.read()
        if not ret:
            raspi_log.log_process("Failed to grab frame")
            break

        # Decode QR codes in the frame
        decoded_objects = decode(img)
        for obj in decoded_objects:
            if obj.data:
                data = obj.data.decode('utf-8')
                send_qr(data,old_data)
                old_data = data

        # Display the image preview (optional)
        # cv2.imshow("code detector", img)
        if cv2.waitKey(1) == ord("q"):
            break

    # Free camera object and exit
    cap.release()
    cv2.destroyAllWindows()
    mqtt_adapter.loop()


def send_qr(message, old_message):
    global topic, time_old
    time_now = datetime.datetime.now()
    result = message

    if old_message != message:
        mqtt_adapter.publish(result, topic)
        raspi_log.log_process(f"Published new QR data: {result}")
        time_old = time_now
    elif (time_now - time_old).seconds >= 10:
        mqtt_adapter.publish(result, topic)
        raspi_log.log_process(f"Republished QR data due to timeout: {result}")
        time_old = time_now


if __name__ == "__main__":
    main()
