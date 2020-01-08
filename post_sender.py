from path_handler import PathHandler
import asyncio
import aiohttp
from files_handler import FileHandler

URL = 'http://localhost:8080/post'


class PostSender(object):

    @staticmethod
    async def send_post(url, name, image, response_path):
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data={
                name: image
            }) as response:
                data = await response.content.read()
                PathHandler.ensure_existence(response_path)
                result_image_path = response_path + '\\' + name
                FileHandler.write_bytes(result_image_path, data)

    # def start_looper(self, futures):
    #     loop = asyncio.get_event_loop()
    #     loop.run_until_complete(asyncio.wait(futures))

    # def sender(self, image_path, result_path):
    #     image = FileHandler.read_bytes(image_path)
    #     self.futures.append(PostSender.send_post(URL, image_path.name, image, result_path))
