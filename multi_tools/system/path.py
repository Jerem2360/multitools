import os
from multi_tools import config
from typing import Union


PathType = Union[str, os.PathLike]


class Path:
    @staticmethod
    def is_bslash(path: PathType):
        return '\\' in path

    @staticmethod
    def is_nslash(path: PathType):
        return '/' in path

    @staticmethod
    def conventionalize(path: PathType):
        conv = config.Path.slash_convention
        result = path.replace('\\', conv)
        return result

    @staticmethod
    def win_path(path: PathType):
        conv = config.Path.win_convention
        result = path.replace('/', conv)
        return result



