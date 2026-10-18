"""
Maximum Split of Positive Even Integers: Closed-Form Count.

1. Dividing everything by 2 turns the task into splitting m = finalSum / 2 into the most distinct
   positive integers. Using 1..k costs k * (k + 1) / 2, so the best count is the largest k with
   k * (k + 1) / 2 <= m.
2. Solve that inequality directly with math.isqrt: k = (isqrt(8 * m + 1) - 1) // 2. Exact integer
   arithmetic, no floating point, so it is safe for very large sums.
3. Build 2, 4, ..., 2k in one range() call and add the leftover to the last element.

Time Complexity: O(sqrt(finalSum)) to build the output (O(1) arithmetic to find k)
Space Complexity: O(sqrt(finalSum)) for the output
"""

from math import isqrt


def maximum_even_split(finalSum: int) -> list[int]:
    """Return a list of unique positive even integers that sum up to finalSum.

    If no valid split exists for finalSum (it is odd, zero or negative), return an empty list.
    """
    if finalSum % 2 != 0 or finalSum <= 0:
        return []

    half = finalSum // 2
    count = (isqrt(8 * half + 1) - 1) // 2  # largest k with k * (k + 1) / 2 <= half
    result = list(range(2, 2 * count + 1, 2))
    result[-1] += finalSum - count * (count + 1)  # leftover keeps the last element the largest
    return result
