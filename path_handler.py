from pathlib import Path


class PathHandler(object):
    @staticmethod
    def ensure_existence(path):
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def ensure_existences(*args):
        for path in args:
            PathHandler.ensure_existence(path)
