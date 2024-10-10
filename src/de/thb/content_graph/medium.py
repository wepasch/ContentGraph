from enum import Enum
from pathlib import Path


class MediaType(Enum):
    TEXT = 0
    AUDIO = 1
    VIDEO = 2


class Medium:
    __name: str
    __type: MediaType
    __file_path: Path

    def __init__(self, name: str, media_type: MediaType, file_path: Path):
        self.__name = name
        self.__type = media_type
        self.__file_path = file_path

    @property
    def name(self) -> str:
        return self.__name

    @property
    def type(self) -> MediaType:
        return self.__type

    @property
    def file_path(self) -> Path:
        return self.__file_path