class FileHandler(object):
    @staticmethod
    def read_bytes(path):
        """
        read bytes from file
        @param path: string, the path to the file
        @return: file content as bytes
        """
        with open(path, 'rb') as file:
            content_bytes = file.read()
        return content_bytes

    @staticmethod
    def write_bytes(path, content):
        """
        write bytes to file
        @param path: string, path for saving the content
        @param content: the content to write to file.
        """
        with open(path, 'wb') as image_from_client:
            image_from_client.write(content)
