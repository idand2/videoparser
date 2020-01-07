from aiohttp import web
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
from PIL import Image
from pathlib import Path
from threading import Thread
from socketserver import ThreadingMixIn
import time
import json

BASE_PATH = r'D:\pycharm\videoparser'
SERVER_IMAGES = BASE_PATH + '\\' + 'server_images'
RESIZE_PATH = BASE_PATH + '\\' + 'resized-images'


def image_resize(imgpath):
    im = Image.open(imgpath)
    newsize = (1500, 300)
    im = im.resize(newsize)
    imgpath = Path(imgpath)
    resized_path = RESIZE_PATH + '\\' + imgpath.name
    im.save(resized_path)
    return resized_path


async def hello(request):
    return web.Response(text="Hello, world")


# web.Request.
async def post_handler(request):
    content_length = int(request.headers['Content-Length'])  # <--- Gets the size of data
    avi_length = request.headers  # <--- Gets the size of data
    avi_defd = await request.read()
    idx = str(avi_defd).find('filename=')
    end_quete_index = str(avi_defd).find('"', idx + 10)
    name = str(avi_defd)[idx + 10: end_quete_index]
    start_of_content_pos = avi_defd.find(b'\r\n\r\n')
    pic = avi_defd[start_of_content_pos + 4:]
    path = SERVER_IMAGES + '\\' + name
    with open(path, 'wb') as lafds:
        lafds.write(pic)
    #        lafds.write(str(post_data) + str(content_length) + '\n' + str(avi_length)+ '\n'+ str(avi_defd))
    resized_path = image_resize(path)
    with open(resized_path, 'rb') as resized :
        resized_image = resized.read()

    return web.Response(body=resized_image)


async def handler(request):
    return web.Response()


app = web.Application()
app.add_routes([web.post('/', post_handler), web.post('/post', post_handler)])

web.run_app(app)
