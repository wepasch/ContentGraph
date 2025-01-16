from enum import Enum

import numpy as np

from de.thb.constants import KEY_NAME
from de.thb.content_graph.graph.node.node_type import NodeType
from de.thb.misc.queryobjects import QueryNode


class ActivityType(Enum):
    __number: int
    __label: str
    __is_meta: bool

    def __init__(self, number: int, label: str, is_meta: bool):
        self.__number = number
        self.__label = label
        self.__is_meta = is_meta

    PHYSICAL = 0, 'Do_Physical_Exercise', False
    VIDEO = 1, 'Watch_Video', False
    USER_INPUT = 2, 'User_Input', False
    AUDIO = 3, 'Listen_To_Audio', False
    OTHER = 4, 'Other_Activity', False
    META = 5, 'Meta_Activity', True

    @property
    def number(self) -> int:
        return self.__number

    @property
    def label(self) -> str:
        return self.__label

    @property
    def is_meta(self) -> bool:
        return self.__is_meta

    @classmethod
    def values(cls, non_meta: bool = False) -> list:
        all_types: list[ActivityType] = list(ActivityType.__members__.values())
        if non_meta:
            return [t for t in all_types if not t.is_meta]
        return all_types

    @classmethod
    def get_query_node(cls, t: 'ActivityType') -> QueryNode:
        return QueryNode(f'{NodeType.TYPE.abbr}_{t.number}', NodeType.TYPE, {
            KEY_NAME: t.label
        })


class ActivityTypeManager:
    __type_to_int: dict[ActivityType, int]

    def __init__(self, types: set[ActivityType]):
        self.__type_to_int = {t: i for i, t in enumerate(types)}

    @property
    def size(self) -> int:
        return len(self.__type_to_int)

    def get_int(self, activity_type: ActivityType) -> int:
        return self.__type_to_int[activity_type]

    def get_arr(self, activity_type: ActivityType) -> np.ndarray[tuple[int, int,], np.dtype[np.bool_]]:
        type_arr: np.ndarray[tuple[int, int,], np.dtype[np.bool_]] = np.zeros((1, len(self.__type_to_int)),
                                                                              dtype=bool)
        type_arr[0][self.get_int(activity_type)] = True
        return type_arr
