from PIL import Image
from pathlib import Path

class ImageHandler(object):
    @staticmethod
    def image_resize(image_path, new_size, resized_path):
        im = Image.open(image_path)
        im = im.resize(new_size)
        image_path = Path(image_path)
        resized_image_path = resized_path + '\\' + image_path.name
        im.save(resized_path)
        return resized_image_path
