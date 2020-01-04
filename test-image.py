# Improting Image class from PIL module
from PIL import Image

# Opens a image in RGB mode


def image_resize(imgpath):

    im = Image.open(imgpath)
    newsize = (1500, 300)
    im = im.resize(newsize)
    im.show()

