from enum import Enum


class NodeType(Enum):
    __label: str
    __abbr: str

    def __init__(self, label: str, abbr: str):
        self.__label = label
        self.__abbr = abbr

    ACTIVITY = 'Activity', 'a'
    DISEASE = 'Disease', 'd'
    TYPE = 'Type', 't'

    @property
    def label(self) -> str:
        return self.__label

    @property
    def abbr(self) -> str:
        return self.__abbr

    @classmethod
    def values(cls) -> list['NodeType']:
        return list(NodeType.__members__.values())


