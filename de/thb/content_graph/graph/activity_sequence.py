import copy

import numpy as np

from typing import Any

from de.thb.content_graph.graph.node.activity_type import ActivityTypeManager
from de.thb.content_graph.graph.node.activity import Activity
from de.thb.content_graph.graph.node.activity_type import ActivityType


class OrderError(Exception):
    """Custom exception for operations in the wrong order."""
    pass


class ActivitySequence:
    __slots__ = ['__uid', '__duration', '__activities', '__matrix', '__size']
    __uid: str
    __activities: list[Activity]
    __duration: int
    __matrix: np.ndarray[Any, np.dtype[np.bool_]]
    __size: int

    def __init__(self, uid: str, nof_activity_types: int):
        self.__uid = uid
        self.__duration = 0
        self.__activities = []
        self.__matrix = np.zeros((0,nof_activity_types), dtype=bool)
        self.__size = 0


    @property
    def uid(self) -> str:
        return self.__uid

    @property
    def duration(self) -> int:
        return self.__duration

    @property
    def matrix(self) -> np.ndarray[tuple[int, int,], np.dtype[np.bool_]]:
        return self.__matrix

    @property
    def size(self) -> int:
        return self.__size

    @property
    def activities_uids(self) -> list[str]:
        return [a.uid for a in self.__activities]

    def last_steps(self, s: int) -> np.ndarray[tuple[int, int,], np.dtype[np.bool_]]:
        return self.__matrix[-s:]

    def get_activities_cp(self) -> list[Activity]:
        return self.__activities

    def duration_at(self, i: int) -> int:
        return sum([a.duration for a in self.__activities[:i + 1]])

    def add_activity(self, activity: Activity, type_arr: np.ndarray[tuple[int, int,], np.dtype[np.bool_]]) -> None:
        self.__activities.append(activity)
        self.__duration += activity.duration
        self.__matrix = np.append(self.__matrix, type_arr, axis=0)
        self.__size += 1

    def __add_activities(self, activities: list[Activity], matrix: np.ndarray[tuple[int, int], np.dtype[np.bool_]],
                         size: int, duration: int) -> None:
        self.__activities = activities
        self.__size = size
        self.__duration = duration
        self.__matrix = matrix

    def __set_duration(self, duration: int) -> None:
        self.__duration = duration

    def __repr__(self) -> str:
        return f'{self.uid}: {'|'.join([a.uid for a in self.__activities])} = {self.__duration}'

    def __copy__(self, uid: str):
        sequence: ActivitySequence = ActivitySequence(uid, self.matrix.shape[1])
        sequence.__add_activities(self.__activities[:], np.copy(self.__matrix), self.__size, self.__duration)
        return sequence


    @classmethod
    def from_activity_sequence(cls, uid: str, activities: tuple[Activity], activity_type_manager: ActivityTypeManager)\
            -> 'ActivitySequence':
        activity_sequence: ActivitySequence = ActivitySequence(uid, activity_type_manager.size)
        for activity in activities:
            activity_sequence.add_activity(activity, activity_type_manager.get_arr(activity.type))
        return activity_sequence




