"""
There is a one-dimensional garden on the x-axis. The garden starts at the point 0 and ends at the point n. 
(i.e., the length of the garden is n).

There are n + 1 taps located at points [0, 1, ..., n] in the garden.

Given an integer n and an integer array ranges of length n + 1 where ranges[i] (0-indexed) means the i-th 
tap can water the area [i - ranges[i], i + ranges[i]] if it was open.

Return the minimum number of taps that should be open to water the whole garden, If the garden cannot be 
watered return -1.
"""

def min_taps(n: int, ranges: list[int]) -> int:
    """Return the minimum number of taps that should be open to water the whole garden.

    If the garden cannot be watered return -1. The input is not modified.

    Raises ValueError if n is negative, if ranges does not have length n + 1,
    or if any range is negative.
    """
    if n < 0:
        raise ValueError("n must be non-negative.")
    if len(ranges) != n + 1:
        raise ValueError("ranges must have length n + 1.")
    if min(ranges) < 0:
        raise ValueError("ranges must not contain negative values.")

    # Create a list of intervals representing the watering range of each tap
    intervals = [(max(0, i - ranges[i]), min(n, i + ranges[i])) for i in range(n + 1)]

    # Sort intervals by their starting point (this sorts our own list, not the caller's)
    intervals.sort(key=lambda interval: interval[0])

    count = 0
    current_end = 0
    next_end = 0
    i = 0
    while current_end < n:
        while i < len(intervals) and intervals[i][0] <= current_end:
            next_end = max(next_end, intervals[i][1])
            i += 1

        if next_end == current_end:
            return -1  # No further progress can be made

        count += 1
        current_end = next_end

    return count
