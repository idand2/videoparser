from aiohttp import web
from files_handler import FileHandler
from image_handler import ImageHandler
from path_handler import PathHandler

BASE_PATH = r'C:\Users\Omer Dayan\PycharmProjects\videoparser'
# BASE_PATH = r'D:\pycharm\videoparser'
SERVER_IMAGES = BASE_PATH + '\\' + 'server_images'
RESIZE_PATH = BASE_PATH + '\\' + 'resized-images'
NEW_SIZE = (1500, 300)


class AsyncServer(object):

    @staticmethod
    async def get_handler(request):
        return web.Response(text="Hey, i'm here for post requests. post me an image and get it in 500X1500")

    @staticmethod
    def validate_initial_path():
        PathHandler.ensure_existences(RESIZE_PATH, SERVER_IMAGES)

    @staticmethod
    def create_temp_image(name, pic):
        path = SERVER_IMAGES + '\\' + name
        FileHandler.write_bytes(path, pic)
        return path

    async def post_handler(self, request):
        self.validate_initial_path()
        request_content = await request.read()
        temp_image_name, temp_image_bytes = self.parse_request(request_content)
        with open(BASE_PATH+'\\avi.jpg', 'wb') as file:
            file.write(temp_image_bytes)
        #temp_image_path = self.create_temp_image(temp_image_name, temp_image_bytes)
        #resized_image_path = ImageHandler.image_resize(temp_image_path, temp_image_name, NEW_SIZE, RESIZE_PATH)
        #resized_image = FileHandler.read_bytes(resized_image_path)
        resized_image = ImageHandler.image_resize(temp_image_bytes, NEW_SIZE)
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
