"""
Reduce Array Size to The Half: Frequency-Bucket Alternative.

1. Counts occurrences of each value with Counter.
2. Buckets the counts by frequency: how many distinct values occur exactly f times, for f = 1..n.
3. Scans frequencies from n down to 1, taking whole groups of equally frequent values at a time.
4. Uses ceil(n / 2) as the target, so odd lengths are handled correctly.
5. Plain module-level function (no stray `self`); never mutates the caller's list.

Time Complexity: O(n), because frequencies are bounded by n and need no comparison sort
Space Complexity: O(n) auxiliary space
"""

from collections import Counter


def min_set_size(arr: list[int]) -> int:
    """Return the fewest distinct values whose removal deletes at least half of arr."""
    n = len(arr)
    target = (n + 1) // 2
    if target == 0:
        return 0

    values_with_frequency = [0] * (n + 1)
    for frequency in Counter(arr).values():
        values_with_frequency[frequency] += 1

    removed = 0
    chosen = 0
    for frequency in range(n, 0, -1):
        available = values_with_frequency[frequency]
        if not available:
            continue
        needed = -(-(target - removed) // frequency)  # ceil division
        take = min(available, needed)
        removed += take * frequency
        chosen += take
        if removed >= target:
            break
    return chosen
