import cv2
import numpy
FILE_TYPE = '.jpg'



class ImageHandler(object):
    @staticmethod
    def image_resize(image_bytes, new_size):
        nparr = numpy.fromstring(image_bytes, numpy.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        resized_image = cv2.resize(image, new_size)
        resized_image_str = cv2.imencode(FILE_TYPE, resized_image)[1].tostring()
        return bytes(resized_image_str)
