"""
You have n flower seeds. Every seed must be planted first before it can begin to grow, then bloom. 
Planting a seed takes time and so does the growth of a seed. You are given two 0-indexed integer arrays 
plantTime and growTime, of length n each:

plantTime[i] is the number of full days it takes you to plant the ith seed. Every day, you can work on 
planting exactly one seed. You do not have to work on planting the same seed on consecutive days, but 
the planting of a seed is not complete until you have worked plantTime[i] days on planting it in total.
growTime[i] is the number of full days it takes the ith seed to grow after being completely planted. 
After the last day of its growth, the flower blooms and stays bloomed forever.
From the beginning of day 0, you can plant the seeds in any order.

Return the earliest possible day where all seeds are blooming 
"""

from operator import itemgetter


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

    # Plant the slowest-growing seeds first: their growth overlaps with the planting of the rest.
    seeds = sorted(zip(plantTime, growTime), key=itemgetter(1), reverse=True)

    current_day = 0  # day on which planting of the current seed finishes
    bloom_day = 0
    for plant, grow in seeds:
        current_day += plant
        bloom_day = max(bloom_day, current_day + grow)

    return bloom_day
