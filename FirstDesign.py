import asyncore
from PIL import Image
import cv2
import os

class EchoHandler(asyncore.dispatcher_with_send):
    def handle_read(self):
        size =  4096000
        data = self.recv(8192)
        a = str(data)
        if a.startswith('SIZE'):
            #self.size = int(a.split()[1])
            self.send('GOT SIZE')
        else:
            data = self.recv(size)
            self.send(data)


class EchoServer(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket()
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accepted(self, sock, addr):
        print('Incoming connection from %s' % repr(addr))
        handler = EchoHandler(sock)


server = EchoServer('localhost', 8080)
asyncore.loop()





def image_resize(imgpath):

    im = Image.open(imgpath)
    newsize = (1500, 300)
    im = im.resize(newsize)
    im.show()



cam = cv2.VideoCapture("D:\Photo\Mufasa.mp4")

try:

    # creating a folder named data
    if not os.path.exists('data'):
        os.makedirs('data')

    # if not created then raise error
except OSError:
    print('Error: Creating directory of data')

# frame
currentframe = 0

while (True):

    # reading from frame
    ret, frame = cam.read()

    if ret:
        # if video is still left continue creating images
        name = './data/frame' + str(currentframe) + '.jpg'
        print('Creating...' + name)

        # writing the extracted images
        cv2.imwrite(name, frame) # TODO: change to send image.

        # increasing counter so that it will
        # show how many frames are created
        currentframe += 1
    else:
        break

#Release all space and windows once done
cam.release()
cv2.destroyAllWindows()




















