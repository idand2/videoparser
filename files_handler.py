class FileHandler(object):
    @staticmethod
    def read_bytes(path):
        with open(path, 'rb') as file:
            content_bytes = file.read()
        return content_bytes

    @staticmethod
    def write_bytes(path, content):
        with open(path, 'wb') as image_from_client:
            image_from_client.write(content)
