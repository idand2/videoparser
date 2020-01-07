from PIL import Image


class ImageHandler(object):
    @staticmethod
    def image_resize(image_path, name, new_size, resized_path):
        im = Image.open(image_path)
        im = im.resize(new_size)
        resized_image_path = resized_path + '\\' + name
        im.save(resized_image_path)
        return resized_image_path
