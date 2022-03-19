from __future__ import print_function

import datetime

from utils import print_table
from pybst.rdbtree import RBTree
import random
import cProfile
import pstats


def insert(bst, arr):
    for value in arr:
        bst.insert(value, value)


def search(bst, n, limit):
    for _ in range(n):
        value = random.randint(0, limit)
        bst.get_node(value)


def test_delete(bst, n, limit):
    for _ in range(n):
        value = random.randint(0, limit)
        bst.delete(value)


if __name__ == "__main__":
    search_iterations = 10000
    n_experiments = 10
    result = []

    for p in range(1, 5):
        unique_values_number = 10**p
        insert_durations = []
        search_durations = []
        for i in range(n_experiments):
            array = [_ for _ in range(unique_values_number)]
            random.shuffle(array)

            bst = RBTree()

            # Test insert complexity
            profiler = cProfile.Profile()
            profiler.enable()
            insert(bst, array)
            profiler.disable()
            total_tt = pstats.Stats(profiler).sort_stats('tottime').total_tt
            insert_durations.append(total_tt)

            # Test search complexity
            profiler = cProfile.Profile()
            profiler.enable()
            search(bst, search_iterations, unique_values_number)
            profiler.disable()
            total_tt = pstats.Stats(profiler).sort_stats('tottime').total_tt
            search_durations.append(total_tt)

        result.append([unique_values_number,
                       datetime.timedelta(seconds=sorted(insert_durations)[int(n_experiments / 2 - 1)]),
                       datetime.timedelta(seconds=sorted(search_durations)[int(n_experiments / 2 - 1)])])

    print_table(['number of values', 'insert duration', 'search duration'], result, 'lcc')
