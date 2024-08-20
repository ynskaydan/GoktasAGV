import cv2
import numpy as np
from pyzbar.pyzbar import decode
import raspi

from CrossCuttingConcerns import raspi_log


def main():

    cap = cv2.VideoCapture(0, cv2.CAP_V4L)

    while True:
        # Kameradan bir kare yakala
        ret, frame = cap.read()
        if not ret:
            print("Kamera görüntüsü alınamadı. Kontrol ediniz!")
            break

        # Pyzbar ile QR kodlarını tespit et ve oku
        decoded_objects = decode(frame)
        for obj in decoded_objects:
            data = obj.data.decode('utf-8')
            raspi_log.log_process(data)
            points = obj.polygon
            if len(points) > 4:
                hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
                points = hull
            n = len(points)
            for j in range(n):
                cv2.line(frame, tuple(points[j]), tuple(points[(j + 1) % n]), (255,0,0), 3)

        cv2.imshow("QR Code Scanner", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":
    main()