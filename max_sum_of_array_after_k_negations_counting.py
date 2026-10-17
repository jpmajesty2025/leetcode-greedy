"""
Maximize Sum After K Negations: Counting Alternative.

1. Counts how many times each value occurs in a list indexed by (value - min), in O(n).
2. Walks the negative values from most negative upward, flipping up to k of them in bulk:
   flipping v adds -2v to the sum, for each copy at once.
3. If flips remain and are odd, subtracts twice the smallest absolute value (a zero costs nothing).
4. Never mutates the caller's list.

Precondition: the value range (max - min) is modest, as in LeetCode's -100..100.

Time Complexity: O(n + R) where R = max(nums) - min(nums) + 1
Space Complexity: O(R) auxiliary space
"""


def largest_sum_after_k_negations(nums: list[int], k: int) -> int:
    """Return the largest array sum reachable by negating one element, exactly k times."""
    lowest = min(nums)
    highest = max(nums)
    counts = [0] * (highest - lowest + 1)
    for value in nums:
        counts[value - lowest] += 1

    total = sum(nums)
    min_abs = min(abs(value) for value in nums)

    value = lowest
    last_negative = min(highest, -1)
    while value <= last_negative and k > 0:
        flips = min(counts[value - lowest], k)
        total -= 2 * value * flips
        k -= flips
        value += 1

    if k % 2 == 1:
        total -= 2 * min_abs
    return total
