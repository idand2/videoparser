# Importing all necessary libraries
import cv2
import time
import asyncio
from pathlib import Path
from files_handler import FileHandler
from path_handler import PathHandler
from post_handler import PostHandler
import sys
import datetime

URL = 'http://localhost:8080/post'
BASE_PATH = r'C:\Users\Omer Dayan\PycharmProjects\videoparser'
# BASE_PATH = r'D:\pycharm\videoparser'
VIDEO_PATH = BASE_PATH + '\\' + 'video\\Mufasa.mp4'
IMAGES_PATH = BASE_PATH + '\\' + 'images'
RESULT_PATH = BASE_PATH + '\\' + 'Result'
FILE_TYPE = '.jpg'


class VideoSplitter(object):
    """
    This class is responsible for splitting the video into frames.
    Adding the frames to a post request and sending the request asynchronously.
    """

    def __init__(self, video_path, result_path):
        self.video_path = video_path
        self.result_path = result_path
        self.tasks = []
        self.validate_initial_path()

    def validate_initial_path(self):
        """
        make sure that the path entered exists, if not creates it recursively
        """
        PathHandler.ensure_existences(self.result_path)

    def create_future_task(self, name, image, result_path):
        """
        appends a task to a list
        @param name: str, the name of the image.
        @param image: str, image file formatted to str.
        @param result_path: the path to saved the response resized image.
        """
        self.tasks.append(PostHandler.handle_post(URL, name, image, result_path))

    def start_async_loop(self):
        """
        start an async loop in order to initiate all tasks .
        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(self.tasks))

    def split_to_frames(self):
        """
        split the video into frames.
        """
        # Read the video from specified path
        video = cv2.VideoCapture(self.video_path)
        current_frame = 0
        done_splitting = False
        while not done_splitting:
            # Reads the video as frames.
            frame_left, frame = video.read()
            # Checks if no frames has been grabbed.
            if frame_left:
                # If video is still left continue creating images
                image_path = Path(IMAGES_PATH + '\\' + 'frame' + str(current_frame) + '.jpg')
                img_str = cv2.imencode('.jpg', frame)[1].tostring()
                self.create_future_task(image_path.name, img_str, self.result_path)
                # increasing counter so that it will
                current_frame += 1
            else:
                done_splitting = True

        # Release all space and windows once done
        video.release()
        cv2.destroyAllWindows()


# def run_test(number_of_instances, seconds_between_runs, video_path):
#     for instance_num in range(1, number_of_instances + 1):
#         print(datetime.datetime.now())
#         instance_result_dir = RESULT_PATH + str(instance_num)
#         # to make it different video add vid_path = sys.argv[3]
#         client = VideoSplitter(video_path, instance_result_dir)
#         asyncio.run(client.splitter())
#         time.sleep(int(seconds_between_runs))
#         print(datetime.datetime.now())
#

def main():
    start_time = time.time()
    client = VideoSplitter(VIDEO_PATH, RESULT_PATH)
    client.split_to_frames()
    client.start_async_loop()
    print("----completed in %s seconds" % (time.time() - start_time))


# def main():
#     n = int(sys.argv[1])
#     m = int(sys.argv[2])
#     vid_path = str(sys.argv[3])
#     start_time = time.time()
#     run_test(n, m, vid_path)
#     print("----all instances are completed in %s seconds" % (time.time() - start_time))


if __name__ == '__main__':
    main()
