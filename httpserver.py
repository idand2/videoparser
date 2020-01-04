#!/usr/bin/env python3
"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
from PIL import Image
from pathlib import Path
from threading import Thread
from socketserver import ThreadingMixIn

BASE_PATH = r'D:\pycharm\videoparser'
SERVER_IMAGES = BASE_PATH + '\\' + 'server_images'
RESIZE_PATH = BASE_PATH + '\\' + 'resized-images'


def image_resize(imgpath):
    im = Image.open(imgpath)
    newsize = (1500, 300)
    im = im.resize(newsize)
    imgpath = Path(imgpath)
    resized_path = RESIZE_PATH + '\\' + imgpath.name
    im.save(resized_path)


class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself
        nameindex = str(post_data).find(r'filename=')
        end_quete_index = str(post_data).find('"', nameindex + 10)
        name = str(post_data)[nameindex + 10:end_quete_index]
        start_of_content_pos = post_data.find(b'\r\n\r\n')
        pic = post_data[start_of_content_pos + 4:]
        path = SERVER_IMAGES + '\\' + name
        with open(path, 'wb') as lafds:
            lafds.write(pic)
        image_resize(path)
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                     str(self.path), str(self.headers), post_data)  # .decode('utf-8'))
        with open((BASE_PATH + '\\' + 'avi.txt'), 'w') as yosi:
            yosi.write(str(post_data))
        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))


# def run(server_class=HTTPServer, handler_class=S, port=8090):
#     logging.basicConfig(level=logging.INFO)
#     server_address = ('localhost', port)
#     httpd = server_class(server_address, handler_class)
#     logging.info('Starting httpd...\n')
#     try:
#         httpd.serve_forever()
#     except KeyboardInterrupt:
#         pass
#     # httpd.server_close()
#     logging.info('Stopping httpd...\n')
def run():
    server = ThreadedHTTPServer(('localhost', 8090), S)
    print('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()


# class ThreadedHTTPServer(HTTPServer):
#     ""


class ThreadedHTTPServer(HTTPServer):
    def process_request(self, request, client_address):
        thread = Thread(target=self.__new_request, args=(self.RequestHandlerClass, request, client_address, self))
        thread.start()

    def __new_request(self, handlerClass, request, address, server):
        handlerClass(request, address, server)
        self.shutdown_request(request)


if __name__ == '__main__':
    run()
