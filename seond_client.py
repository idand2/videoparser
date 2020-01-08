# Importing all necessary libraries
import cv2
import time
import asyncio
from pathlib import Path
from files_handler import FileHandler
from path_handler import PathHandler
from post_sender import PostSender
import sys
import datetime

URL = 'http://localhost:8080/post'
BASE_PATH = r'C:\Users\Omer Dayan\PycharmProjects\videoparser'
# BASE_PATH = r'D:\pycharm\videoparser'
VIDEO_PATH = BASE_PATH + '\\' + 'video\\Mufasa.mp4'
IMAGES_PATH = BASE_PATH + '\\' + 'images'
RESULT_PATH = BASE_PATH + '\\' + 'Result'


class VideoSplitter(object):
    """
    this class is responsible for splitting the video into frames.
    """

    def __init__(self, video_path, result_path):
        self.video_path = video_path
        self.result_path = result_path
        self.futures = []
        PathHandler.ensure_existence(result_path)
        PathHandler.ensure_existence(IMAGES_PATH)

    @staticmethod
    def write_frame(current_frame, frame):
        """
        writing result frame as bytes
        :param current_frame: int , for naming.
        :param frame: Image, contains the data to be written
        :return: path , the path of the saved image.
        """
        path = Path(IMAGES_PATH + '\\' + 'frame' + str(current_frame) + '.jpg')
        print('Creating...' + str(path))
        cv2.imwrite(str(path).replace('\\\\', '\\'), frame)
        return path

    def create_futures(self, image_path, result_path):
        image = FileHandler.read_bytes(image_path)
        self.futures.append(PostSender.send_post(URL, image_path.name, image, result_path))

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
                self.create_futures(path, self.result_path)
                # increasing counter so that it will
                current_frame += 1
            else:
                frame_left_in_video = False

        # Release all space and windows once done
        cam.release()
        cv2.destroyAllWindows()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(self.futures))
        # return self.futures


def run_test(number_of_instances, seconds_between_runs, video_path):

    #for instance_num in range(1, number_of_instances + 1):
        print(datetime.datetime.now())
        instance_result_dir = RESULT_PATH + str(instance_num)
        # to make it different video add vid_path = sys.argv[3]
        client = VideoSplitter(video_path, instance_result_dir)
        client.splitter()
    #
    # time.sleep(int(seconds_between_runs))
    # print(datetime.datetime.now())


# def main():
#     start_time = time.time()
#     client = VideoSplitter(VIDEO_PATH, RESULT_PATH)
#     client.splitter()
#     # PostSender.start_looper(a)
#     print("----completed in %s seconds" % (time.time() - start_time))


def main():
    n = int(sys.argv[1])
    m = int(sys.argv[2])
    vid_path = str(sys.argv[3])
    start_time = time.time()
    run_test(n, m, vid_path)
    print("----all instances are completed in %s seconds" % (time.time() - start_time))


if __name__ == '__main__':
    main()
