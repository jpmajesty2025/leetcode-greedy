"""
Earliest Possible Day of Full Bloom: Group Seeds by Grow Time.

1. Seeds with the same grow time are interchangeable for the answer: only the last one planted in
   the group matters, and by then all of the group's planting time has been spent. So each group
   can be collapsed into one entry: (total planting days in the group, grow time).
2. Sort only the distinct grow times, descending, instead of all n seeds.
3. Walk the groups: add the group's planting days, then the bloom day of the group is that running
   total plus its grow time. The answer is the largest of these.

This is the same greedy as sorting every seed, but it sorts k distinct grow times, not n seeds.
It is a good fit when many seeds share the same growth time.

Time Complexity: O(n + k log k), where k is the number of distinct grow times
Space Complexity: O(k)
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

    plant_by_grow: dict[int, int] = {}
    for plant, grow in zip(plantTime, growTime):
        plant_by_grow[grow] = plant_by_grow.get(grow, 0) + plant

    current_day = 0
    bloom_day = 0
    for grow in sorted(plant_by_grow, reverse=True):
        current_day += plant_by_grow[grow]
        bloom_day = max(bloom_day, current_day + grow)
    return bloom_day
