import cv2
import numpy

FILE_TYPE = '.jpg'


class ImageHandler(object):

    @staticmethod
    def reconvert_string_to_image(image_string):
        """
        @param image_string: an image reformatted as string
        @return: Image object
        """
        nparr = numpy.fromstring(image_string, numpy.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return image

    @staticmethod
    def image_resize(image_string, new_size):
        """
        Resizes image using CPU for now :)
        @param image_string:string,  an image reformatted as string
        @param new_size: tuple, the image new resolution as tuple of ints.
        @return: bytes, image as bytes.
        """
        image = ImageHandler.reconvert_string_to_image(image_string)
        resized_image = cv2.resize(image, new_size)
        resized_image_str = cv2.imencode(FILE_TYPE, resized_image)[1].tostring()
        return bytes(resized_image_str)
