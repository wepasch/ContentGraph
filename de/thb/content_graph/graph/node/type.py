from enum import Enum


class MediumType(Enum):
    __name: str

    def __init__(self, name: str):
        self.__name = name

    UNKNOWN = 'n.A.'
    TEXT = 'text'
    AUDIO = 'audio'
    VIDEO = 'video'

    @property
    def name(self) -> str:
        return self.__name

    @staticmethod
    def get(s: str) -> 'MediumType':
        if not s:
            return MediumType.UNKNOWN
        s_l: str = s.casefold()
        if s_l in ['text', 't']:
            return MediumType.TEXT
        elif s_l in ['audio', 'a']:
            return MediumType.AUDIO
        elif s_l in ['video', 'v']:
            return MediumType.VIDEO
        else:
            return MediumType.UNKNOWN


class NodeType(Enum):
    __label: str
    __ref: str

    def __init__(self, label: str, ref: str):
        self.__label = label
        self.__ref = ref

    ACTIVITY = 'Activity', 'a'
    MEDIUM = 'Medium', 'm'
    DISEASE = 'Disease', 'd'
    THERAPY = 'Therapy', 't'
    META = 'Meta', 'x'

    @property
    def label(self) -> str:
        return self.__label

    @property
    def ref(self) -> str:
        return self.__ref

    @classmethod
    def values(cls) -> list['NodeType']:
        return list(NodeType.__members__.values())


class RelationType(Enum):
    __label: str

    def __init__(self, label: str):
        self.__label = label

    PATH = 'path'
    REQUIRES = 'requires'
    SUITABLE = 'suitable'
    USES = 'uses'

    @property
    def label(self) -> str:
        return self.__label



