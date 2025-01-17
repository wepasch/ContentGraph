import itertools
import pickle
from functools import reduce

import numpy as np

from de.thb.content_graph.graph.activity_sequence import ActivitySequence
from de.thb.content_graph.graph.app.sequence_validator import SequenceValidator, ValidatorConfig
from de.thb.content_graph.graph.node.activity import Activity


#validator_config: ValidatorConfig = ValidatorConfig((3, 3), (10, 30), (3, 5), 2)
#access: Neo4jAccess = Neo4jAccess.get_access()
#all_activities: list[Activity] = access.get_nodes_like(QueryNode('', NodeType.ACTIVITY))
#activities: list[Activity] = [] #[a for a in all_activities if not a.type.is_meta]
with open('activities.nps', 'rb') as file:
    pass#activities = pickle.load(file)



def find_sequences(s: ActivitySequence, available_activities: list[Activity], validator: SequenceValidator, depth_counter: int,
                   collected: list[ActivitySequence]) -> None:
    for i in range(len(available_activities)):
        a: Activity = available_activities[i]
        t = s.__copy__(f's_{depth_counter}_{i}')
        t.add_activity(a, validator.manager.get_arr(a.type))
        if not validator.is_valid(t, ignore_min=True):
            continue
        if t.size >= validator.config.min_size and t.duration >= validator.config.min_duration:
            collected.append(t.__copy__(t.uid))
        find_sequences(t, available_activities[:i] + available_activities[i + 1:], validator, depth_counter + 1, collected)


def find_permuts(elements: set[str], collected: set[tuple[str,...]]):
    for element in elements:
        for t in collected:
            collected.add(t + (element,))
        find_permuts(elements - {element}, collected | {element})



def find_permutations(seq: tuple[tuple[str,...], int], au: set[str], lu: dict[str, int], ms: tuple[int, int],
                      mt: tuple[int, int,], cs: set[tuple[str,...]]) -> None:
    sl: int = len(seq[0])
    if sl >= ms[1]:
        return
    for u in au:
        nt: int = seq[1] + lu[u]
        if nt > mt[1]:
            continue
        if nt >= mt[0] and (sl + 1) >= ms[0]:
            cs.add(seq[0] + (u,))
        find_permutations((seq[0] + (u,), nt), au - {u}, lu, ms, mt, cs)


def collect_boxed_matrices(matrix: np.ndarray[tuple[int, int,], np.dtype[np.bool_]], acc_time: int,
                           time_lu: tuple[int, ...], depth: int, config: ValidatorConfig,
                           cs: list[np.ndarray[tuple[int, int,], np.dtype[np.bool_]]]) -> None:
    if depth >= config.max_size:
        return
    done_vector: np.ndarray[tuple[int,], np.dtype[np.bool_]] = ~np.any(matrix[:depth], axis=0)
    open_indices: np.ndarray[tuple[int,], np.dtype[np.bool_]] = np.where(done_vector)[0].astype(np.uint8)
    c: np.uint8
    for c in open_indices:
        next_matrix = np.copy(matrix)
        next_time: int = acc_time + time_lu[c.item()]
        if next_time > config.max_duration:
            continue
        next_matrix[depth][c.item()] = True
        if config.min_duration <= next_time and config.min_size <= (depth + 1):
            cs.append(np.copy(next_matrix))
        collect_boxed_matrices(next_matrix, next_time, time_lu, depth + 1, config, cs)


def type_matrix_invalid(matrix: np.ndarray[tuple[int, int,], np.dtype[np.bool_]], last_row: int) -> bool:
    limit: int = 3
    var: tuple[int, int,] = (3, 5)
    x = np.sum(matrix[-limit:], axis=0)
    if np.any(x >= limit):
        return False
    y = np.any(matrix[max(0, last_row - var[1]):last_row], axis=0).astype(np.bool_)
    z = np.sum(y).astype(np.uint8)
    min_var = min(last_row, var[0])
    if z < min_var:
        return False
    return True


def collect_valid_matrices(matrix: np.ndarray[tuple[int, int,], np.dtype[np.bool_]],
                           type_matrix: np.ndarray[tuple[int, int,], np.dtype[np.bool_]],
                           time_lu: tuple[int, ...], type_lu: tuple[int, ...], acc_time: int, depth: int,
                           config: ValidatorConfig,
                           cs: list[np.ndarray[tuple[int, int,], np.dtype[np.bool_]]]) -> None:
    if depth >= config.max_size:
        return
    done_vector: np.ndarray[tuple[int,], np.dtype[np.bool_]] = ~np.any(matrix[:depth], axis=0)
    open_indices: np.ndarray[tuple[int,], np.dtype[np.uint8]] = np.where(done_vector)[0].astype(np.uint8)
    c: np.uint8
    for c in open_indices:
        next_type_matrix = np.copy(type_matrix).astype(np.bool_)
        next_type_matrix[depth][type_lu[c.item()]] = True
        if not type_matrix_invalid(next_type_matrix, depth + 1):
            continue
        next_matrix: np.ndarray[tuple[int, int,], np.dtype[np.bool_]] = np.copy(matrix).astype(np.bool_)
        next_time: int = acc_time + time_lu[c.item()]
        if next_time > config.max_duration:
            continue
        next_matrix[depth][c.item()] = True
        if config.min_duration <= next_time and config.min_size <= (depth + 1):
            cs.append(np.copy(next_matrix))
        collect_valid_matrices(next_matrix, next_type_matrix, time_lu, type_lu, next_time, depth + 1, config, cs)


def create_boxed_permutations(base: set[str], n: int, lu: dict[str, int], tm: int) -> set[tuple[str, ...]]:
    combos = itertools.combinations(base, n)
    timed_combos = filter(lambda c: tm > sum(map(lambda u: lu[u], c)), combos)
    perms = reduce(lambda a, c: a | set(itertools.permutations(c)), timed_combos, set())
    return perms


def write_boxed_tensors(activities: list[Activity], seq_len: int):
    validator_config: ValidatorConfig = ValidatorConfig((3, seq_len), (10, 30), (3, 5), 2)
    tlu = {a.uid: a.duration for a in activities}
    cols = []
    collect_boxed_matrices(np.zeros((validator_config.max_size, len(tlu)), dtype=np.bool_), 0, tuple([a.duration for a in activities]), 0,
                           validator_config, cols)
    tensor = np.array(cols)
    with open(f'tensor_{validator_config.min_size}_{validator_config.max_size}_{validator_config.min_duration}_{validator_config.max_duration}.nps', 'wb') as file:
        np.save(file, tensor)

def write_valid_tensors(activities: list[Activity], seq_len: int):
    validator_config: ValidatorConfig = ValidatorConfig((3, seq_len), (10, 40), (3, 5), 2)
    nof_activities: int = len({a.uid: a.duration for a in activities})
    type_lu: tuple[int, ...] = tuple([a.type.number for a in activities])
    nof_types: int = len({a.type.number for a in activities})
    cols = []
    collect_valid_matrices(np.zeros((validator_config.max_size, nof_activities), dtype=np.bool_),
                           np.zeros((validator_config.max_size, nof_types), dtype=np.bool_),
                           tuple([a.duration for a in activities]), type_lu,
                           0, 0, validator_config, cols)
    tensor = np.array(cols)
    with open(f'tensor_{validator_config.min_size}_{validator_config.max_size}_{validator_config.min_duration}_{validator_config.max_duration}.nps', 'wb') as file:
        np.save(file, tensor)
