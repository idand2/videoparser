import cv2
import time
import asyncio
from path_handler import PathHandler
from post_handler import PostHandler
import logging
import platform

URL = 'http://localhost:8080/post'
# BASE_PATH = r'C:\Users\Omer Dayan\PycharmProjects\videoparser'
WIN_BASE_PATH = r'D:\pycharm\videoparser'
# WIN_BASE_PATH = r'C:\temp\videoparser'
LINUX_BASE_PATH = '/etc/temp/'
LINUX_RESULT_PATH = LINUX_BASE_PATH + '/Results'
WIN_VIDEO_PATH = WIN_BASE_PATH + '\\' + 'video\\Mufasa.mp4'
LINUX_VIDEO_PATH = LINUX_BASE_PATH + '/video/Mufasa.mp4'
FILE_TYPE = '.jpg'
WIN_RESULT_PATH = WIN_BASE_PATH + '\\' + 'Results'


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
                frame_name = ('frame' + str(current_frame) + '.jpg')
                img_str = cv2.imencode('.jpg', frame)[1].tostring()
                self.create_future_task(frame_name, img_str, self.result_path)
                # increasing counter so that it will
                current_frame += 1
            else:
                done_splitting = True

        # Release all space and windows once done
        video.release()
        cv2.destroyAllWindows()


def is_linux():
    """
    check if the type of the os is linux.
    :return: Boolean.
    """
    os = platform.system()
    if 'Linux' == os:
        return True

    elif 'Windows' == os:
        return False


def main():
    """
    initiate client, log total runtime to file.
    :return:
    """
    start_time = time.time()
    if is_linux():
        client = VideoSplitter(LINUX_VIDEO_PATH, LINUX_RESULT_PATH)
    else:
        client = VideoSplitter(WIN_VIDEO_PATH, WIN_RESULT_PATH)
    client.split_to_frames()
    client.start_async_loop()
    logging.basicConfig(filename="anyvision.log", filemode='w', level=logging.DEBUG,
                        format="[%(asctime)s] [%(levelname)s] [%(message)s]")
    logging.info("Completed in %s seconds" % str(time.time() - start_time)[:4])


if __name__ == '__main__':
    main()
