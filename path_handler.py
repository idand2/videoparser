from pathlib import Path


class PathHandler(object):
    @staticmethod
    def ensure_existence(path):
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)
