import os
from http.server import SimpleHTTPRequestHandler, HTTPServer

from constants import Constants


class CustomHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('index.html', 'rb') as file:
                self.wfile.write(file.read())
        elif self.path.startswith('/send/'):
            message = self.path.split('/')[-1]
            if Constants.develop_mode == True:
                os.system(
                    f"mosquitto_pub -t move -h localhost -m {message} ")
            else:
                os.system(
                    f"mosquitto_pub -t move -h {Constants.ip_addr} -m {message} -u {Constants.mqtt_username} -P {Constants.mqtt_password}")

            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            # self.wfile.write(f"'{message}' mesajı gönderildi.".encode())
            print(f"'{message}' message send.".encode())
        else:
            self.send_error(404, "File not found.")


def run(server_class=HTTPServer, handler_class=CustomHandler):
    server_address = (Constants.ip_addr, 8000)
    httpd = server_class(server_address, handler_class)
    print('Server running on port 8000...')
    httpd.serve_forever()


if __name__ == '__main__':
    run()
