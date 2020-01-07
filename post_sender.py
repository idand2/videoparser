from path_handler import PathHandler
import asyncio
import aiohttp
from pathlib import Path
from files_handler import FileHandler


class PostSender(object):
    @staticmethod
    async def send_post(url, name, image, response_path):
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data={
                name: image
            }) as response:
                data = await response.content.read()
                PathHandler.ensure_existence(response_path)
                saving_path = response_path + '\\' + name
                FileHandler.write_bytes(saving_path, data)
