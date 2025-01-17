import heapq
import logging
from itertools import combinations

import numpy as np

from de.thb.content_graph.graph.activity_sequence import ActivitySequence
from de.thb.content_graph.graph.node.activity import Activity
from de.thb.content_graph.graph.node.activity_type import ActivityTypeManager

logger = logging.getLogger(__name__)


class ValidatorConfig:
    __size_range: tuple[int, int,]
    __time_range: tuple[int, int,]
    __variety: tuple[int, int]
    __repetition_limit: int

    def __init__(self, size_range: tuple[int, int,] = (0,0), time_range: tuple[int, int,] = (0,0),
                 variety: tuple[int, int] = (0,0), repetition_limit: int = 1):
        if size_range[0] > size_range[1] or time_range[1] < 0:
            raise ValueError(f"Size range is {size_range}")
        if time_range[0] > time_range[1] or time_range[1] < 0:
            raise ValueError(f"Time range is {time_range}")
        if variety[0] > variety[1] or variety[1] < 0:
            raise ValueError(f"Variety is {variety}")
        if repetition_limit < 1:
            raise ValueError(f"Repetition limit is {repetition_limit}")
        self.__size_range = size_range
        self.__time_range = time_range
        self.__variety = variety
        self.__repetition_limit = repetition_limit

    @property
    def min_size(self) -> int:
        return self.__size_range[0]

    @property
    def max_size(self) -> int:
        return self.__size_range[1]

    @property
    def min_duration(self) -> int:
        return self.__time_range[0]

    @property
    def max_duration(self) -> int:
        return self.__time_range[1]

    @property
    def variety_count(self) -> int:
        return self.__variety[0]

    @property
    def window_size(self) -> int:
        return self.__variety[1]

    @property
    def repetition_limit(self) -> int:
        return self.__repetition_limit

    def is_valid_duration(self, duration: int) -> bool:
        return self.min_duration <= duration <= self.max_duration

    def is_valid_size(self, size: int) -> bool:
        return self.min_size <= size <= self.max_size


class SequenceValidator:
    __activities: list[Activity]
    __activity_manager: ActivityTypeManager
    __config: ValidatorConfig

    def __init__(self, activities: list[Activity], config: ValidatorConfig):
        self.__activities = activities
        self.__config = config
        self.__activity_manager = ActivityTypeManager({a.type for a in activities})


    @property
    def activities(self) -> list[Activity]:
        return self.__activities

    @property
    def manager(self) -> ActivityTypeManager:
        return self.__activity_manager

    @property
    def config(self) -> ValidatorConfig:
        return self.__config

    def is_valid_duration(self, duration: int) -> bool:
        return self.config.min_duration <= duration <= self.config.max_duration

    def is_valid_size(self, size: int) -> bool:
        return self.config.min_size <= size <= self.config.max_size

    def get_max_sequence_length(self) -> int:
        shortest_activities: list[Activity] = heapq.nsmallest(self.config.max_size, [a for a in self.activities
                                                                                     if not a.type.is_meta],
                                                              key=lambda a: a.duration)
        shortest_path_duration: int = sum([a.duration for a in shortest_activities])
        if shortest_path_duration <= self.config.max_duration:
            logger.info(f'Max path length restricted by max number of activities: {self.config.max_size}')
            return self.config.max_size
        rm_activities: int = 1
        while self.config.max_size < sum([a.duration for a in shortest_activities[:-rm_activities]]):
            rm_activities += 1
        max_length: int = self.config.max_size - rm_activities
        logger.info(f'Max path length restricted by max time: {max_length}')
        return max_length

    def get_sequence_tuples(self) -> list[tuple[Activity]]:
        sequences: list[tuple[Activity]] = []
        n: int
        for n in range(self.config.min_size, self.get_max_sequence_length() + 1):
            new_sequences: list[tuple[Activity]] = list(combinations(self.activities, n))
            sequences += new_sequences
            logger.info(f'Added {len(new_sequences)} sequences of length {n}.')
        return sequences

    def get_valid_sequences(self) -> list[ActivitySequence]:
        boxed_activity_sequences: list[ActivitySequence] = self.get_boxed_activity_sequences()
        logger.info(f'Identified {len(boxed_activity_sequences)} sized and timed activity sequences.')
        limited_activity_sequences: list[ActivitySequence] = [s for s in boxed_activity_sequences if not self.has_repetition(s)]
        logger.info(f'Identified {len(limited_activity_sequences)} activity sequences without too many repetition.')
        valid_activity_sequences: list[ActivitySequence] = [s for s in limited_activity_sequences if self.has_variation(s)]
        logger.info(f'Identified {len(valid_activity_sequences)} valid activity sequences.')
        return valid_activity_sequences

    def get_boxed_activity_sequences(self) -> list[ActivitySequence]:
        all_activity_sequences: list[tuple[Activity]] = self.get_sequence_tuples()
        logger.info(f'Combined to {len(all_activity_sequences)} activity sequences.')
        timed_activity_sequences: list = [s for s in all_activity_sequences if self.is_valid_duration(sum([a.duration for a in s]))]
        activity_sequences: list[ActivitySequence] = [ActivitySequence.from_activity_sequence(f's_{len(s)}_{i}', s, self.manager) for i, s in enumerate(timed_activity_sequences)]
        return activity_sequences

    def has_repetition(self, activity_sequence: ActivitySequence) -> bool:
        acc = np.zeros((1, activity_sequence.matrix.shape[1]), dtype=np.int8)
        for row in activity_sequence.matrix:
            SequenceValidator.cooldown_add(row, acc)
            if np.any(acc > self.config.repetition_limit):
                return True
        return False

    def has_variation(self, activity_sequence: ActivitySequence) -> bool:
        matrix: np.ndarray[tuple[int, int,], np.dtype[np.bool_]] = activity_sequence.matrix
        for i in range(0, matrix.shape[0] + 1 - self.config.window_size):
            if not SequenceValidator.col_check(matrix[:][i:i + self.config.window_size], self.config.variety_count):
                return False
        return True

    def is_valid(self, activity_sequence: ActivitySequence, ignore_min: bool = False) -> bool:
        if not self.is_valid_size(activity_sequence.size):
            if not ignore_min or activity_sequence.size > self.config.max_size:
                return False
        if not self.is_valid_duration(activity_sequence.duration):
            if not ignore_min or activity_sequence.duration > self.config.max_duration:
                return False
        if self.has_repetition(activity_sequence):
            return False
        return self.has_variation(activity_sequence)

    @staticmethod
    def col_check(matrix: np.ndarray[tuple[int, int,], np.dtype[np.bool_]], required: int) -> bool:
        return len(np.any(matrix, axis=0)) >= required

    @staticmethod
    def cooldown_add(summand: np.ndarray[tuple[int,], np.dtype[np.bool_]],
                     target: np.ndarray[tuple[int, int,], np.dtype[np.int8]]) -> None:
        for i in range(target.shape[1]):
            s_i: np.bool_ = summand[i]
            t_i: np.int8 = target[0][i]
            amt: int = 1 if s_i or t_i else 0
            sig: int = -1 if not s_i and t_i else 1
            target[0][i] += sig * amt
