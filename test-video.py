# Importing all necessary libraries
import cv2
import os
import requests
import time
import asyncio
import aiohttp

URL = 'http://localhost:8090'
VIDEO_PATH = r'D:\Photo\Mufasa.mp4'
BASE_PATH = r'D:\pycharm\videoparser'
IMAGES_PATH = BASE_PATH + '\\' + 'images'

# for path, subddir, files in os.walk(args['folder']):
#     for f_name in files:
#         futures.append(send_file(path, f_name))






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
            # increasing counter so that it will
            # show how many frames are created
            currentframe += 1
        else:
            break

    # Release all space and windows once done
    cam.release()
    cv2.destroyAllWindows()


# def async send_post


start_time = time.time()
avi()




async def send_file(path1):
    # url = args['url']
    async with aiohttp.ClientSession() as session:
        async with session.post(URL, data={
            'file': open(path1, 'rb')
        }) as response:
            data = await response.text()
            print(data)

# async def post_image(url, path):
#     files = {'media': open(path, 'rb')}
#     requests.post(url, files=files)

def set_future_right():
    done_files = []
    futures = []
    images = os.listdir(IMAGES_PATH)
    if len(images) == 0:
        'congrats, we are done.'
    else:
        for i in images:
            if len(futures) > 100:
                break
            else:
                futures.append(send_file((IMAGES_PATH + '\\' + i)))
                done_files.append(IMAGES_PATH + '\\' + i)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(futures))
        print(done_files)
        for ipath in done_files:
            os.remove(ipath) #TODO : think about images.remove()
        set_future_right()


set_future_right()

print("----completed in %s seconds" % (time.time() - start_time))
