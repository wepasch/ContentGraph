import math
import matplotlib
import random

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

from de.thb.content_graph.neo_4_j.activity_generator import get_activities_from
from de.thb.content_graph.graph.node.activity import Activity
from de.thb.content_graph.graph.node.activity_type import ActivityType

matplotlib.use('TkAgg')

REP_LIMIT: int = 2
VARIETY: tuple[int, int,] = (3, 5)
SCORES_WEIGHT: tuple[float, float, float,] = (0.45, 0.45, 0.1,)
SCORES_PEN: tuple[float, float, float,] = (3, 3, 1,)
SCORE_NAMES: list[str] = ['repetition', 'variety', 'variance', 'mean']
SCORE_COLORS: list[str] = ['red', 'blue', 'orange', 'green']
SCORE_POINTS: list[str] = ['.', '.', '.', 'o']




def plot_with_matrix(scores: list[list[float]], matrix: np.ndarray[tuple[int, int,], np.dtype[np.bool]],
                     title: str = 'Scores up to k and type matrix', only_last: bool = False) -> None:
    """
    Creates plot with scores on the left and the schematic representation of the bool matrix.
    """
    rows, cols = matrix.shape
    ks: range = range(1, rows + 1)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    for idx, score in enumerate(scores):
        if only_last and idx != len(scores) - 1:
            continue
        ax1.plot(ks, score, label=SCORE_NAMES[idx], marker=SCORE_POINTS[idx], color=SCORE_COLORS[idx])
    ax1.set_title(title)
    ax1.set_xlabel('k')
    ax1.set_ylabel('Scores')
    ax1.legend(loc='best')
    ax1.grid(axis='y', alpha=0.3)


    ax2.imshow(matrix, cmap='Greys', interpolation='none')
    for i in range(rows):
        for j in range(cols):
            rect = Rectangle((j - 0.5, i - 0.5), 1, 1, fill=False, edgecolor='black', linewidth=1)
            ax2.add_patch(rect)
        if i % 5 == 4 or i == 0:
            ax2.text(-1, i, str(i  + 1), va='center', ha='right', fontsize=10, color='black')
    ax2.axis('off')
    ax2.set_xlim(-0.5, cols - 0.5)
    ax2.set_ylim(rows - 0.5, -0.5)
    ax2.set_aspect('equal', adjustable='box')

    plt.tight_layout()
    plt.show()


def draw_matrix(matrix: np.ndarray[tuple[int, int,], np.dtype[np.bool]]) -> None:
    """
    Draws schematic representation of the bool matrix.
    """
    plt.imshow(matrix, cmap='Greys', interpolation='none')
    ax = plt.gca()
    rows, cols = matrix.shape
    for i in range(rows):
        for j in range(cols):
            rect = Rectangle((j - 0.5, i - 0.5), 1, 1, fill=False, edgecolor='black', linewidth=1)
            ax.add_patch(rect)
    plt.axis('off')
    plt.show()



def plot_scores(scores: list[list[float]], title: str = 'Scores up to k', only_last: bool = False) -> None:
    """
    Plots lists in scores in one graph.
    :param only_last: only plots last list in scores
    """
    nof_scores: int = len(scores)
    nof_values: int = len(scores[0])
    ks: range = range(1, nof_values + 1)

    plt.figure(figsize=(8, 4))
    for i, series in enumerate(scores):
        if only_last and i != nof_scores - 1:
            continue
        plt.plot(ks, series, marker=SCORE_POINTS[i], linestyle='-', label=SCORE_NAMES[i], color=SCORE_COLORS[i])
    plt.title(title)
    plt.xlabel('k')
    plt.ylabel('Scores')
    plt.ylim(0, 1)
    plt.legend()
    plt.grid(alpha=0.6)
    plt.show()


def with_mean(scores: list[tuple[float, float, float,]]) -> list[tuple[float, float, float, float,]]:
    """
    Adds the mean of the existing entries in the tuples to the tuple.
    """
    return [t + (calc_mean(t),) for t in scores]


def tuples_to_series(tuples: list[tuple[float,...]]) -> list[list[float]]:
    """
    Converts a list of tuples into a list of lists. All tuple entries with index i are combined in one list.
    """
    return [[t[t_i] for t in tuples] for t_i in range(len(tuples[0]))]

def tuple_lists_to_series(tuple_lists: list[list[tuple[float,...]]]) -> list[list[list[float]]]:
    """
    Converts list of tuple lists into lists of lists. All tuple entries with index i are combined in one list.
    """
    return [tuples_to_series(tl) for tl in tuple_lists]

def plot_scores_list(scores_list: list[list[list[float]]], title: str = 'Scores up to k',
                     only_last: bool = False) -> None:
    """
    Plots multiple score lists. If the score_list has n entries, a square of length floor(sqrt(n)) is created with
    plots. E.g. with 3 entries a square 2x2 is plotted consisting of three actual plots and one empty slot in
    the square.
    """
    nof_scores_sets: int = len(scores_list)
    if nof_scores_sets == 1:
        plot_scores(scores_list[0], title=title, only_last=only_last)
        return
    nof_scores: int = len(scores_list[0])
    nof_values: int = len(scores_list[0][0])
    width: int = math.ceil(math.sqrt(nof_scores_sets))
    ks: range = range(1, nof_values + 1)

    fig, axes = plt.subplots(width, width, figsize=(10, 10), constrained_layout=True)

    for i in range(width):
        for j in range(width):
            scores_idx: int = i * width + j
            if scores_idx >= nof_scores_sets:
                break
            ax = axes[i, j]
            for k, score in enumerate(scores_list[scores_idx]):
                if only_last and k != nof_scores - 1:
                    continue
                ax.plot(ks, score, marker=SCORE_POINTS[k], linestyle='-', label=SCORE_NAMES[k], color=SCORE_COLORS[k])
                ax.set_ylim(0, 1)
    plt.show()


def calc_matrix_scores(matrix: np.ndarray[tuple[int, int,], np.dtype[np.bool]],
                       mean: bool = False) -> list[tuple[float, float, float,]] | list[tuple[float, float, float, float,]]:
    """
    Calculates scores for each submatrix (from 1 to matrix.shape[0]) of a given matrix as tuples. The score of the
    whole matrix is in the last tuple.
    :param mean : If True, the mean is added to each tuple
    """
    scores: list[tuple[float, float, float,]] = [eval_matrix(matrix[:r + 1], mean=mean) for r in range(matrix.shape[0])]
    return scores


def activities_to_type(done_activities: list[Activity], type_lu: dict[ActivityType, int]) -> (
        np.ndarray[tuple[int, int,], np.dtype[np.bool]]):
    """
    Converts an activity list into a bool matrix using the type_lu dictionary, which indicates the index (col) of an
    activity's type in the bool array.
    """
    type_matrix: np.ndarray[tuple[int, int,], np.dtype[np.bool]] = (np.zeros((len(done_activities), len(type_lu)))
                                                                    .astype(np.bool))
    for ai, a in enumerate(done_activities):
        type_matrix[ai][a.type.number] = True
    return type_matrix


def get_random_bool_matrix(shape: tuple[int, int,]) -> np.ndarray[tuple[int, int,], np.dtype[np.bool]]:
    """
    :return: 2d bool matrix with given shape
    """
    matrix: np.ndarray[tuple[int, int,], np.dtype[np.bool]] = np.zeros(shape, dtype=bool)
    h = [random.randint(0, shape[1] - 1) for _ in range(shape[0])]
    for r, c in enumerate(h):
        matrix[r][c] = True
    return matrix


def apply_bool(ints: np.ndarray[tuple[int,], np.dtype[np.int16]],
               bools: np.ndarray[tuple[int,], np.dtype[np.bool]]) -> None:
    """
    Increments column in ints if bool in same is True. Decreases column in ints if corresponding bool is False.
    Minimum in ints is 0.
    """
    for c in range(ints.shape[0]):
        if bools[c]:
            ints[c] += 1
        elif ints[c] > 0:
            ints[c] -= 1


def get_max_std(shape: tuple[int, int,]) -> float:
    """
    Calculates the maximum standard deviation of a bool matrix w/ exactly one True entry in each row. A matrix w/
    True entries in only one column has a column sum vector of [m, 0, 0, ...] with m = number of rows and n = number of columns.
    µ = m / n
    max_variance = ((m - µ)^2 + ((n - 1) * µ^2)) / n
    max_std = sqrt(max_variance)
    """
    quo: float = shape[0] / shape[1]
    var_pre = (shape[0] - quo)**2 + (shape[1] - 1) * quo**2
    var = var_pre / shape[1]
    return math.sqrt(var)


def calc_mean(t: tuple[float, float, float], weights: tuple[float, float, float,] = SCORES_WEIGHT) -> float:
    """
    Calculates the mean of a given tuple using the given weights or standard weights.
    """
    return weights[0] * t[0] + weights[1] * t[1] + weights[2] * t[2]


def glo_score(matrix: np.ndarray[tuple[int, int,], np.dtype[np.bool]]) -> float:
    """
    Sums True values of columns into integer vector. The std of the values of that vector is calculated.
    The actual std is converted in to a number between 0 and pi/2. E.g.:
    std = 0 -> 0
    std = 0.5 max_std -> pi/4
    std = max_std -> pi/2
    The glo score is the cos of the resulting number. So for small stds the penalty is small. While std near the max_std
    result in low scores.
    """
    cols_sums: np.ndarray[tuple[int,], np.dtype[np.uint8]] = np.sum(matrix, axis=0)
    std: np.floating = np.std(cols_sums)
    max_std: float = get_max_std(matrix.shape)
    return round(math.cos((std * math.pi) / (2 * max_std)) if max_std != 0 else 1, 4)


def var_score(matrix: np.ndarray[tuple[int, int,], np.dtype[np.bool]]) -> float:
    """
    VARIETY[0] -> min number of types
    VARIETY[1] -> frame size
    Counts how often in the last 'frame size' entries less than min number of types are present while walking throw the
    rows of the matrix. For each occurrence the score is decreased by SCORES_PEN[1]^-1 (min: 0).
    No penalty for the first VARIETY[1] rows only if they are of different types.
    Alternative: decrease penalty the bigger the matrix is.
    """
    counter: int = 0
    for r in range(1, matrix.shape[0] + 1):
        used_cols: np.ndarray[tuple[int,], np.dtype[np.bool]] = (np.any(matrix[max(0, r - VARIETY[1]):r], axis=0)
                                                                 .astype(np.bool))
        variety: np.uint8 = np.sum(used_cols).astype(np.uint8)
        if min(r, VARIETY[0]) > variety:
            counter += 1
    sc: float = 1 - (counter / SCORES_PEN[1])
    return sc if sc > 0 else 0
    #return (1 - counter / matrix.shape[0])**2


def rep_score(matrix: np.ndarray[tuple[int, int,], np.dtype[np.bool]]) -> float:
    sum_row: np.ndarray[tuple[int,], np.dtype[np.int16]] = np.zeros((matrix.shape[1],), dtype=np.int16)
    """
        VARIETY[0] -> min number of types
        VARIETY[1] -> frame size
        Counts how often a columns counter exceeds REP_LIMIT. For each occurrence the score is decreased by 
        SCORES_PEN[0]^-1 (min: 0).
        Alternative: decrease penalty the bigger the matrix is.
        """
    counter: int = 0
    for r in range(matrix.shape[0]):
        apply_bool(sum_row, matrix[r])
        if np.any(sum_row > REP_LIMIT):
            counter += 1
    sc: float = 1 - (counter / SCORES_PEN[0])
    return sc if sc > 0 else 0
    #return (1 - counter / matrix.shape[0])**2

def matrix_str_rep(matrix:  np.ndarray[tuple[int, int,], np.dtype[np.bool]]) -> str:
    """
    :return: matrix representation made of X and O (True/False)
    """
    s: str = ''
    for r in matrix:
        for c in r:
            s += 'X' if c else 'O'
        s += '\\n'
    return s


def eval_matrix(matrix, mean: bool = False) -> tuple[float, float, float,] | tuple[float, float, float, float, ]:
    """
    Calculates score once for the whole matrix.
    :param mean: add mean to score tuple
    """
    if mean:
        scores = (rep_score(matrix), var_score(matrix), glo_score(matrix))
        return scores + (calc_mean(scores),)
    else:
        return rep_score(matrix), var_score(matrix), glo_score(matrix)


def plot_bins(data_points: list[float], title: str = 'Histogram of Values', x_label: str = 'score value',
             y_label: str = 'frequency', bins: int = 33, x_range: tuple[int, int,] = (0, 1)) -> None:
    """
    Puts given data_points into bins and plots a bar chart.
    """
    plt.hist(data_points, bins=bins, range=x_range, color='skyblue', edgecolor='black', alpha=0.7)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid(axis='y', alpha=0.6)
    plt.show()


def eval_activity_sequence(activity_sequence: list[Activity], type_lu: dict[ActivityType, int],
                           mean: bool = False) -> tuple[float, float, float,] | tuple[float, float, float, float]:
    """
    Converts activities into type bool matrix and calculates the score of the resulting matrix (w/ or w/o mean)
    """
    matrix: np.ndarray[tuple[int, int,], np.dtype[np.bool]] = activities_to_type(activity_sequence, type_lu)
    return eval_matrix(matrix, mean)


def show_some(delayed_score: bool = False) -> None:
    """
    Generates random bool matrices, plot the progression of their scores from 1 to matrix.shape[0] and
    draws representation of matrix next to plot.
    Closing a plot starts generation of a new from a new matrix.
    """
    while True:
        matrix: np.ndarray[tuple[int, int,], np.dtype[np.bool]] = get_random_bool_matrix((25, 5))
        scores = calc_matrix_scores(matrix, mean=True)
        score_lists = tuples_to_series(scores)
        if delayed_score:
            draw_matrix(matrix)
            plot_with_matrix(score_lists, matrix)
        else:
            plot_with_matrix(score_lists, matrix)
