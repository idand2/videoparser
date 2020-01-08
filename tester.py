from async_client import VideoSplitter
import asyncio
import datetime
import time
import sys

BASE_PATH = r'D:\pycharm\videoparser'
VIDEO_PATH = BASE_PATH + '\\' + 'video\\Mufasa.mp4'
RESULT_PATH = BASE_PATH + '\\' + 'Result'
a = VideoSplitter(VIDEO_PATH, RESULT_PATH)
futures = a.splitter()
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(futures))


def run_test(number_of_instances, seconds_between_runs, video_path):
    loop = asyncio.get_event_loop()
    for instance_num in range(1, number_of_instances + 1):
        print(datetime.datetime.now())
        instance_result_dir = RESULT_PATH + str(instance_num)
        # to make it different video add vid_path = sys.argv[3]
        client = VideoSplitter(video_path, instance_result_dir)
        futures = await client.splitter()
        asyncio.wait(futures)
        time.sleep(int(seconds_between_runs))
        print(datetime.datetime.now())


def main():
    n = int(sys.argv[1])
    m = int(sys.argv[2])
    vid_path = str(sys.argv[3])
    start_time = time.time()
    run_test(n, m, vid_path)
    print("----all instances are completed in %s seconds" % (time.time() - start_time))


if __name__ == '__main__':
    main()
