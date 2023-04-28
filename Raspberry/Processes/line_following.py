def main():
    import cv2
    import numpy as np
    # Kamera ayarları
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    while True:
        # Görüntü yakalama
        ret, frame = camera.read()

        # Görüntüyü gri tonlamaya çevirme
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Görüntüyü eşikleme
        ret, thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)

        # Görüntüyü filtreleme
        kernel = np.ones((3, 3), np.uint8)
        thresh = cv2.erode(thresh, kernel, iterations=2)
        thresh = cv2.dilate(thresh, kernel, iterations=2)

        # Contours bulma
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # En büyük contouru bulma
        max_area = 0
        max_contour = None
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > max_area:
                max_area = area
                max_contour = contour

        # En büyük contourun merkezini bulma
        if max_contour is not None:
            M = cv2.moments(max_contour)
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

            # Çizgiyi takip etme
            if cx < 300:
                print("Sola dön")
            elif cx > 340:
                print("Sağa dön")
            else:
                print("İleri git")

        # Görüntüyü gösterme
        cv2.imshow("frame", frame)

        # Çıkış için q tuşuna basılması
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # Temizleme
    camera.release()
    cv2.destroyAllWindows()


main()
