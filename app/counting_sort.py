import datetime
import random
import cProfile
import pstats

from utils import print_table


# source: https://stackabuse.com/counting-sort-in-python/
def counting_sort(inputArray):
    # Find the maximum element in the inputArray
    maxElement = max(inputArray)

    countArrayLength = maxElement+1

    # Initialize the countArray with (max+1) zeros
    countArray = [0] * countArrayLength

    # Step 1 -> Traverse the inputArray and increase
    # the corresponding count for every element by 1
    for el in inputArray:
        countArray[el] += 1

    # Step 2 -> For each element in the countArray,
    # sum up its value with the value of the previous
    # element, and then store that value
    # as the value of the current element
    for i in range(1, countArrayLength):
        countArray[i] += countArray[i-1]

    # Step 3 -> Calculate element position
    # based on the countArray values
    outputArray = [0] * len(inputArray)
    i = len(inputArray) - 1
    while i >= 0:
        currentEl = inputArray[i]
        countArray[currentEl] -= 1
        newPosition = countArray[currentEl]
        outputArray[newPosition] = currentEl
        i -= 1

    return outputArray


def timsort(arr):
    # Python uses Timsort algorithm https://en.wikipedia.org/wiki/Timsort
    return sorted(arr)


def measure(arr: list, n_experiments: int = 10) -> dict:
    counting_sort_durations = []
    timsort_durations = []

    for _ in range(n_experiments):
        profiler = cProfile.Profile()
        profiler.enable()
        array1 = counting_sort(arr)
        profiler.disable()
        total_tt = pstats.Stats(profiler).sort_stats('tottime').total_tt
        counting_sort_durations.append(total_tt)

        profiler = cProfile.Profile()
        profiler.enable()
        array2 = timsort(arr)
        profiler.disable()
        total_tt = pstats.Stats(profiler).sort_stats('tottime').total_tt
        timsort_durations.append(total_tt)

        assert(array1 == array2)

    counting_sort_duration = datetime.timedelta(seconds=sorted(counting_sort_durations)[int(n_experiments / 2 - 1)])
    timsort_duration = datetime.timedelta(seconds=sorted(timsort_durations)[int(n_experiments / 2 - 1)])

    return {'countingsort': counting_sort_duration, 'timsort': timsort_duration}


if __name__ == '__main__':
    elements = []
    table_data = []
    for i in range(1, 6):
        array_len = 10**i
        array = [_ for _ in range(array_len)]
        random.shuffle(array)
        duration = measure(array)
        elements.append(array_len)
        table_data.append((f'{array_len} elements', duration['countingsort'], duration['timsort']))

    arr_type = []
    table_data_2 = []
    for num in (10, 1000, 100000):
        duration = measure([1, num])
        arr_type.append(f'[1, {num}]')
        table_data_2.append((f'[1, {num}]', duration['countingsort'], duration['timsort']))

    print_table(['array', 'counting sort', 'timsort'], table_data, 'lcc')
    print_table(['array', 'counting sort', 'timsort'], table_data_2, 'lcc')
