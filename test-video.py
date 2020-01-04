# Importing all necessary libraries
import cv2
import os
import requests

URL = 'http://localhost:8090'
VIDEO_PATH = r'D:\Photo\Mufasa.mp4'

def post_image(url, path):
    files = {'media': open(path, 'rb')}
    requests.post(url, files=files)


def avi():
    # Read the video from specified path
    cam = cv2.VideoCapture(VIDEO_PATH)

    try:

        # creating a folder named data
        if not os.path.exists('images'):
            os.makedirs('images')

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
            name = './images/frame' + str(currentframe) + '.jpg'
            print('Creating...' + name)

            # writing the extracted images
            cv2.imwrite(name, frame)  # TODO: change to send image.
            post_image(URL, name)

            # increasing counter so that it will
            # show how many frames are created
            currentframe += 1
        else:
            break

    # Release all space and windows once done
    cam.release()
    cv2.destroyAllWindows()

avi()
