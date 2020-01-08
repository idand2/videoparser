from pathlib import Path


class PathHandler(object):

    @staticmethod
    def ensure_existence(path):
        """
        checks if path exist if not creates it recursively
        :param path:
        """
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def ensure_existences(*args):
        """
        checks if path exist if not creates it recursively when the num of paths given is unknown.
        :param args: string, paths.
        """
        for path in args:
            PathHandler.ensure_existence(path)
