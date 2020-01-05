# Importing all necessary libraries
import cv2
import os
import requests
import time
import asyncio
import aiohttp
from pathlib import Path

URL = 'http://localhost:8090'
#URL = 'http://localhost:5000'
VIDEO_PATH = r'D:\Photo\Mufasa.mp4'
BASE_PATH = r'D:\pycharm\videoparser'
IMAGES_PATH = BASE_PATH + '\\' + 'images'


# for path, subddir, files in os.walk(args['folder']):
#     for f_name in files:
#         futures.append(send_file(path, f_name))


class VideoSpliter(object):
    def __init__(self, video_path, sender):
        self.video_path = video_path
        self.sender = sender
        self.futures = []
        self.splitter()

    def splitter(self):

        # Read the video from specified path
        cam = cv2.VideoCapture(self.video_path)

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
                path = './images/frame' + str(currentframe) + '.jpg'
                name = Path(path).name
                print('Creating...' + str(path))

                # writing the extracted images
                cv2.imwrite(path, frame)  # TODO: change to send image.
                with open(path, 'rb') as image:
                    self.futures.append(self.sender.send_post(name, image.read()))

                # increasing counter so that it will
                # show how many frames are created
                currentframe += 1
            else:
                break

        # Release all space and windows once done
        cam.release()
        cv2.destroyAllWindows()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(self.futures))


# def async send_post

class PostSender(object):
    def __init__(self, url):
        self.url = url

    async def send_post(self, name, image):
        async with aiohttp.ClientSession() as session:
            async with session.post(URL, data={
                name : image
            }) as response:
                data = await response.text()
                print(data)


start_time = time.time()
b = PostSender(URL)
a = VideoSpliter(VIDEO_PATH, b)

#
# async def send_file(path1):
#     # url = args['url']
#     async with aiohttp.ClientSession() as session:
#         async with session.post(URL, data={
#             'file': open(path1, 'rb')
#         }) as response:
#             data = await response.text()
#             print(data)
#
#
# async def post_image(url, path):
#     files = {'media': open(path, 'rb')}
#     requests.post(url, files=files)
#
# def set_future_right():
#     done_files = []
#     futures = []
#     images = os.listdir(IMAGES_PATH)
#     if len(images) == 0:
#         'congrats, we are done.'
#     else:
#         for i in images:
#             if len(futures) > 100:
#                 break
#             else:
#                 futures.append(send_file((IMAGES_PATH + '\\' + i)))
#                 done_files.append(IMAGES_PATH + '\\' + i)
#
#         loop = asyncio.get_event_loop()
#         loop.run_until_complete(asyncio.wait(futures))
#         print(done_files)
#         for ipath in done_files:
#             os.remove(ipath)  # TODO : think about images.remove()
#         set_future_right()
#
#
# set_future_right()

print("----completed in %s seconds" % (time.time() - start_time))
