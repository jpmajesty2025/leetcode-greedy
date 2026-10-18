"""
Earliest Possible Day of Full Bloom: Bucket by Grow Time (No Comparison Sort).

1. Allocate one bucket per possible grow time, 0..max(growTime), holding the total planting days of
   the seeds with that grow time.
2. Sweep the buckets from the largest grow time down to 0, keeping a running total of planting
   days. Each non-empty bucket finishes blooming at running total + its grow time.
3. The answer is the largest of those bloom days.

Replaces the O(n log n) sort with a counting pass, which is faster when the grow times are bounded
and small (LeetCode: at most 10**4), but needs O(max growTime) memory, so it is a poor fit for
huge grow times.

Time Complexity: O(n + max(growTime))
Space Complexity: O(max(growTime))
"""


def earliest_full_bloom(plantTime: list[int], growTime: list[int]) -> int:
    """Return the earliest possible day where all seeds are blooming.

    The inputs are not modified.

    Raises ValueError if plantTime and growTime have different lengths, if either is empty,
    or if any time is negative.
    """
    if len(plantTime) != len(growTime):
        raise ValueError("plantTime and growTime must have the same length.")
    if not plantTime:
        raise ValueError("plantTime and growTime must not be empty.")
    if min(plantTime) < 0 or min(growTime) < 0:
        raise ValueError("plantTime and growTime must not contain negative values.")

    plant_total = [0] * (max(growTime) + 1)
    occupied = [False] * len(plant_total)
    for plant, grow in zip(plantTime, growTime):
        plant_total[grow] += plant
        occupied[grow] = True

    current_day = 0
    bloom_day = 0
    for grow in range(len(plant_total) - 1, -1, -1):
        if occupied[grow]:
            current_day += plant_total[grow]
            bloom_day = max(bloom_day, current_day + grow)
    return bloom_day
