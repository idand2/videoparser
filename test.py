import asyncore

import cv2
VIDEO = "D:\Photo\Mufasa.mp4"

class HTTPClient(asyncore.dispatcher):

    def __init__(self, host, data):
        asyncore.dispatcher.__init__(self)

        self.create_socket()
        self.connect((host, 8080))
        self.data = data
        self.size = len(self.data)
        # self.buffer = bytes('GET %s HTTP/1.0\r\nHost: %s\r\n\r\n' %
        #                   (path, host), 'ascii')

    def handle_connect(self):
        pass

    def handle_close(self):
        self.close()
    def save_to_file(self):
        pass

    def handle_read(self):
        ans = self.recv(8192)
        if str(ans).startswith('GOT'):
            self.send(self.data)
        else:
            data = self.recv(self.size)
            self.save_to_file()


    def writable(self):
        return (len(self.data) > 0)

    def handle_write(self):
        sent = self.send(self.data)
        self.data = self.data[sent:]

#
# client = HTTPClient('localhost', '/')
# asyncore.loop()


class Image(object):
    def __init__(self, path):
        self.path = path
        self.size = None
        self.data = None

    def read_image(self):
        with open(self.path, 'rb') as img:
            self.data = img.read()
            self.size = len(self.data)





class VideoParser(object):
    def __init__(self, video):
        self.video = video
        self.cam = cv2.VideoCapture(self.video)
        self.currentframe = 0
        self.parse()

    def parse(self):
        while (True):

            # reading from frame
            ret, frame = self.cam.read()

            if ret:
                # if video is still left continue creating images
                name = './data/frame' + str(self.currentframe) + '.jpg'
                print('Creating...' + name)

                # writing the extracted images
                #cv2.imwrite(name, frame)  # TODO: cahnge to socket.send.
                client = HTTPClient('localhost', bytes(frame))
                asyncore.loop()

                # increasing counter so that it will
                # show how many frames are created
                self.currentframe += 1
            else:
                break
            self.cam.release()
            cv2.destroyAllWindows()

# Release all space and windows once done
image = VideoParser(VIDEO)
