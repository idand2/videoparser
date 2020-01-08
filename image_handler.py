from PIL import Image
import cv2
import numpy


def trysw(image_bytes, new_size):
    nparr = numpy.fromstring(str(image_bytes), numpy.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    cv2.resize(image, new_size)


BASE_PATH = r'C:\Users\Omer Dayan\PycharmProjects\videoparser'


class ImageHandler(object):
    @staticmethod
    def image_resize(image_bytes, new_size):
        nparr = numpy.fromstring(image_bytes, numpy.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        resized_image = cv2.resize(image, new_size)
        resized_image_str = cv2.imencode('.jpg', resized_image)[1].tostring()
        return bytes(resized_image_str)

        # im = Image.open(image_path)
        # im = im.resize(new_size)
        # resized_image_path = resized_path + '\\' + name
        # im.save(resized_image_path)
        # return resized_image_path
