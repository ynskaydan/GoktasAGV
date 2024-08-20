import cv2
import numpy as np
from pyzbar.pyzbar import decode

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
            print("QR Code Detected!")
            print("Data:", obj.data.decode('utf-8'))  # QR kodundan alınan veriyi yazdır

            # QR kod çevresine bir dikdörtgen çiz
            points = obj.polygon
            if len(points) > 4:
                hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
                points = hull
            n = len(points)
            for j in range(n):
                cv2.line(frame, tuple(points[j]), tuple(points[(j + 1) % n]), (255,0,0), 3)

        # Görüntüyü göster
        cv2.imshow("QR Code Scanner", frame)

        # 'q' tuşuna basıldığında döngüden çık
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Kamera aygıtını serbest bırak ve tüm OpenCV pencerelerini kapat
    cap.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":
    main()