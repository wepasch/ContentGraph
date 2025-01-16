from enum import Enum


class RelationType(Enum):
    __label: str

    def __init__(self, label: str):
        self.__label = label

    REQUIRES = 'requires'
    SUITABLE = 'suitable'
    PREFERRED = 'preferred'
    IS_A = 'is_a'

    @property
    def label(self) -> str:

        return self.__label
