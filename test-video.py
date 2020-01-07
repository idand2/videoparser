# Importing all necessary libraries
import cv2
import os
import requests
import time
import asyncio
import aiohttp
from pathlib import Path
import

# for path, subddir, files in os.walk(args['folder']):
#     for f_name in files:
#         futures.append(send_file(path, f_name))


class VideoSpliter(object):
    def __init__(self, video_path, sender):
        self.video_path = video_path
        self.sender = sender
        self.futures = []

    @staticmethod
    def write_image(current_frame, frame):
        path = Path(IMAGES_PATH + '\\'+'frame' + str(current_frame) + '.jpg')
        print('Creating...' + str(path))
        # writing the extracted image
        cv2.imwrite(str(path).replace('\\\\', '\\'), frame)
        return path

    @staticmethod
    def file_reader(path):
        with open(path, 'rb') as image:
            image_bytes = image.read()
        return image_bytes

    def splitter(self):

        # Read the video from specified path
        cam = cv2.VideoCapture(self.video_path)
        PostSender.path_handler(IMAGES_PATH)
        # frame
        current_frame = 0
        frame_left_in_video = True
        while frame_left_in_video:
            # reading from frame
            ret, frame = cam.read()  # TODO : figure out what ret means and change the name
            if ret:
                # if video is still left continue creating images
                # TODO: change to send image.
                path = self.write_image(current_frame, frame)
                image = self.file_reader(path)
                self.futures.append(self.sender.send_post(path.name, image))
                # increasing counter so that it will
                current_frame += 1
            else:
                frame_left_in_video = False

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
                name: image
            }) as response:
                data = await response.content.read()
                resized_path = RESIZED_BACK
                self.path_handler(resized_path)
                saving_path = resized_path + '\\' + name
                with open(saving_path, 'wb') as theyareback:
                    theyareback.write(data)

    @staticmethod
    def path_handler(path):
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)


# todo : put in main

def main():
    start_time = time.time()
    sender = PostSender(URL)
    client = VideoSpliter(VIDEO_PATH, sender)
    client.splitter()
    print("----completed in %s seconds" % (time.time() - start_time))


if __name__ == '__main__':
    main()

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
