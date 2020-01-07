from aiohttp import web
from files_handler import FileHandler
from image_handler import ImageHandler
from path_handler import PathHandler

# BASE_PATH = r'C:\Users\Omer Dayan\PycharmProjects\videoparser'
BASE_PATH = r'D:\pycharm\videoparser'
SERVER_IMAGES = BASE_PATH + '\\' + 'server_images'
RESIZE_PATH = BASE_PATH + '\\' + 'resized-images'
NEW_SIZE = (1500, 300)


class AsyncServer(object):

    @staticmethod
    async def get_handler(request):
        return web.Response(text="Hey, i'm here for post requests. post me an image and get it in 500X1500")

    async def post_handler(self, request):
        PathHandler.ensure_existence(SERVER_IMAGES)
        PathHandler.ensure_existence(RESIZE_PATH)
        request_content = await request.read()
        name, pic = self.parse_request(request_content)
        path = SERVER_IMAGES + '\\' + name
        FileHandler.write_bytes(path, pic)
        resized_path = ImageHandler.image_resize(path, name, NEW_SIZE, RESIZE_PATH)
        resized_image = FileHandler.read_bytes(resized_path)
        return web.Response(body=resized_image)

    @staticmethod
    def parse_request(request_content):
        name_start_index = str(request_content).find('filename=')
        end_quete_index = str(request_content).find('"', name_start_index + 10)
        name = str(request_content)[name_start_index + 10: end_quete_index]
        start_of_content_pos = request_content.find(b'\r\n\r\n')
        pic = request_content[start_of_content_pos + 4:]
        return name, pic


def main():
    server = AsyncServer()
    app = web.Application()
    app.add_routes([web.post('/post', server.post_handler)])
    web.run_app(app)


if __name__ == '__main__':
    main()
