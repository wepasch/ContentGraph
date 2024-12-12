from enum import Enum


class ActivityType(Enum):
    __label: str

    def __init__(self, label: str):
        self.__label = label

    PHYSICAL = 'Do_Physical_Exercise'
    VIDEO = 'Watch_Video'
    USER_INPUT = 'User_Input'
    AUDIO = 'Listen_To_Audio'
    OTHER = 'Other_Activity'
    META = 'Meta_Activity'

    @property
    def label(self) -> str:
        return self.__label

    @classmethod
    def values(cls) -> list['ActivityType']:
        return list(ActivityType.__members__.values())
