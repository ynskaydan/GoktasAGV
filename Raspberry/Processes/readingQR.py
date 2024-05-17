import cv2


def main():
    # Kamerayı başlat
    cap = cv2.VideoCapture(0)

    # Çözünürlüğü ayarla
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # QR kodu algılayıcıyı oluştur
    qr_code_detector = cv2.QRCodeDetector()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # QR kodunu tespit et ve çöz
        data, bbox, _ = qr_code_detector.detectAndDecode(frame)

        # Eğer bir QR kodu tespit edilirse
        if bbox is not None:
            for i in range(len(bbox)):
                # QR kodu çevresine dikdörtgen çiz
                cv2.line(frame, tuple(bbox[i][0]), tuple(bbox[(i + 1) % len(bbox)][0]), (0, 255, 0), 2)

            # QR kodun içeriğini ekrana yazdır
            if data:
                cv2.putText(frame, data, (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (0, 255, 0), 2)

        # Görüntüyü göster
        cv2.imshow('QR Code Scanner', frame)

        # 'q' tuşuna basarak çık
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
