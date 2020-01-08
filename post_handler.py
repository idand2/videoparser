from path_handler import PathHandler
import asyncio
import aiohttp
from files_handler import FileHandler

URL = 'http://localhost:8080/post'


class PostHandler(object):
    @staticmethod
    def response_handler(response_path, name, data):
        PathHandler.ensure_existence(response_path)
        result_image_path = response_path + '\\' + name
        FileHandler.write_bytes(result_image_path, data)

    @staticmethod
    async def handle_post(url, name, image, response_path):
        """
        creating and sending post request, saving the response data to file.
        @param url: string, the send destination
        @param name: string, the image name
        @param image: string, the image reformatted as string.
        @param response_path: string, the path to save the resized image.
        @return:
        """
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data={
                name: image
            }) as response:
                data = await response.content.read()
                PostHandler.response_handler(response_path, name, data)
