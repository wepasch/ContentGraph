from enum import Enum


class NodeType(Enum):
    __label: str

    def __init__(self, label: str):
        self.__label = label

    ACTIVITY = 'Activity'
    DISEASE = 'Disease'

    @property
    def label(self) -> str:
        return self.__label

    @classmethod
    def values(cls) -> list['NodeType']:
        return list(NodeType.__members__.values())


class RelationType(Enum):
    __label: str

    def __init__(self, label: str):
        self.__label = label

    REQUIRES = 'requires'
    SUITABLE = 'suitable'
    USES = 'uses'

    @property
    def label(self) -> str:
        return self.__label



