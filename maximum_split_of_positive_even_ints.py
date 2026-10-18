"""
You are given an integer finalSum. Split it into a sum of a maximum number of unique positive even integers.

For example, given finalSum = 12, the following splits are valid (unique positive even integers 
summing up to finalSum): (12), (2 + 10), (2 + 4 + 6), and (4 + 8). Among them, (2 + 4 + 6) contains 
the maximum number of integers. Note that finalSum cannot be split into (2 + 2 + 4 + 4) as all the 
numbers should be unique.
Return a list of integers that represent a valid split containing a maximum number of integers. If 
no valid split exists for finalSum, return an empty list. You may return the integers in any order.
"""

def maximum_even_split(finalSum: int) -> list[int]:
    """Return a list of unique positive even integers that sum up to finalSum.

    If no valid split exists for finalSum (it is odd, zero or negative), return an empty list.
    The input is not modified, and the result is in increasing order.
    """
    if finalSum % 2 != 0 or finalSum <= 0:
        return []

    result = []
    remaining = finalSum
    current_even = 2

    # Greedily take 2, 4, 6, ... while they fit
    while remaining >= current_even:
        result.append(current_even)
        remaining -= current_even
        current_even += 2

    # The leftover is even and smaller than the next even number, so adding it to the
    # largest element keeps every value unique. (result is non-empty: finalSum >= 2.)
    if remaining > 0:
        result[-1] += remaining

    return result
