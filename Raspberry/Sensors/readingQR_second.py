from time import sleep
import zbar
from picamera import PiCamera


def main():
    with PiCamera() as camera:
        camera.start_preview()
        sleep(2)
        with zbar.Scanner() as scanner:
            while True:
                camera.capture('qr_code.jpg')
                image = open('qr_code.jpg', 'rb').read()
                results = scanner.scan(image)
                for result in results:
                    print(result.data.decode('utf-8'))


main()

#sudo apt-get update
#sudo apt-get install libzbar0
#sudo apt-get install libzbar-dev
#sudo pip3 install zbar-py

