from aiohttp import web
from image_handler import ImageHandler

IMAGE_NEW_SIZE = (1500, 300)


class AsyncServer(object):

    @staticmethod
    async def get_handler(request):
        return web.Response(text="Hey, i'm here for post requests. post me an image and get it in 500X1500")

    async def post_handler(self, request):
        """
        handle post requests asynchronously.
        @param request: bytes, the request itself, coming from the client.
        @return: bytes, the response, resized_image as bytes.
        """
        request_content = await request.read()
        temp_image_name, temp_image_bytes = self.parse_request(request_content)
        resized_image = ImageHandler.image_resize(temp_image_bytes, IMAGE_NEW_SIZE)
        return web.Response(body=resized_image)

    @staticmethod
    def parse_request(request_content):
        """
        parse the post request content
        @param request_content: bytes, the request content
        @return: str,bytes: the name of the frame, the frame in str
        """
        name_start_index = str(request_content).find('filename=')
        end_quote_index = str(request_content).find('"', name_start_index + 10)
        name = str(request_content)[name_start_index + 10: end_quote_index]
        start_of_content_pos = request_content.find(b'\r\n\r\n')
        pic = request_content[start_of_content_pos + 4:]
        return name, pic


def main():
    """
    initiate the server using aiohttp.web
    """
    server = AsyncServer()
    app = web.Application()
    app.add_routes([web.get('/', server.get_handler), web.post('/post', server.post_handler)])
    web.run_app(app)


if __name__ == '__main__':
    main()
