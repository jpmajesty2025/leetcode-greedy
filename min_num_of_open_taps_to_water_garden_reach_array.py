"""
Minimum Number of Taps to Open to Water a Garden: Furthest-Reach Array (O(n), No Sorting).

1. Tap i covers [i - ranges[i], i + ranges[i]]. Clamp the left end to 0 and the right end to n.
2. reach[left] = the furthest right end of any tap whose left end is exactly `left`. Left ends are
   integers in 0..n, so this bucketing replaces the sort.
3. Sweep positions 0..n-1 once, tracking the furthest point any tap seen so far can reach.
   When the sweep reaches the end of the watered area, we must open one more tap: the one that
   reaches furthest. If it reaches no further than we are, there is a gap: -1.

Same greedy as the sorted version (a jump game), with the sort replaced by bucketing.

Time Complexity: O(n)
Space Complexity: O(n)
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

    reach = [0] * (n + 1)
    for i, r in enumerate(ranges):
        left = max(0, i - r)
        reach[left] = max(reach[left], min(n, i + r))

    count = 0
    watered_end = 0  # right end of the area watered by the taps opened so far
    furthest = 0     # furthest point one more tap could reach
    for position in range(n):
        furthest = max(furthest, reach[position])
        if position == watered_end:
            if furthest <= position:
                return -1
            count += 1
            watered_end = furthest
            if watered_end >= n:
                break
    return count
