# Importing all necessary libraries
import cv2
import os
import requests
import time
import asyncio
import aiohttp
from pathlib import Path
from files_handler import FileHandler
from path_handler import PathHandler
from post_sender import PostSender

# URL = 'http://localhost:8090'
URL = 'http://localhost:8080'
# URL = 'http://localhost:5000'
BASE_PATH = r'C:\Users\Omer Dayan\PycharmProjects\videoparser'
VIDEO_PATH = BASE_PATH + '\\' + 'video\\Mufasa.mp4'
# VIDEO_PATH = r'D:\Photo\Mufasa.mp4'
# BASE_PATH = r'D:\pycharm\videoparser'
IMAGES_PATH = BASE_PATH + '\\' + 'images'
RESULT_PATH = BASE_PATH + '\\' + 'Result'


# for path, subddir, files in os.walk(args['folder']):
#     for f_name in files:
#         futures.append(send_file(path, f_name))


class VideoSpliter(object):
    def __init__(self, video_path):
        self.video_path = video_path
        self.futures = []
        PathHandler.ensure_existence(IMAGES_PATH)

    @staticmethod
    def write_frame(current_frame, frame):
        path = Path(IMAGES_PATH + '\\' + 'frame' + str(current_frame) + '.jpg')
        print('Creating...' + str(path))
        # writing the extracted image
        cv2.imwrite(str(path).replace('\\\\', '\\'), frame)
        return path

    def splitter(self):
        # Read the video from specified path
        cam = cv2.VideoCapture(self.video_path)
        current_frame = 0
        frame_left_in_video = True
        while frame_left_in_video:
            # reading from frame
            ret, frame = cam.read()  # TODO : figure out what ret means and change the name
            if ret:
                # if video is still left continue creating images
                # TODO: change to send image.
                path = self.write_frame(current_frame, frame)
                image = FileHandler.read_bytes(path)
                self.futures.append(PostSender.send_post(URL, path.name, image, RESULT_PATH))
                # increasing counter so that it will
                current_frame += 1
            else:
                frame_left_in_video = False

        # Release all space and windows once done
        cam.release()
        cv2.destroyAllWindows()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(self.futures))


def main():
    start_time = time.time()
    client = VideoSpliter(VIDEO_PATH)
    client.splitter()
    print("----completed in %s seconds" % (time.time() - start_time))


if __name__ == '__main__':
    main()
