"""
Maximize Sum After K Negations: Sorted Greedy.

1. Sorts a copy, so the caller's list is untouched.
2. Negates the most negative numbers first, at most k of them.
3. If negations remain, every number is now non-negative. An even count of leftovers cancels out;
   an odd count must be spent flipping the element with the smallest absolute value.
4. Finds that element with min(), not a second sort.

Time Complexity: O(n log n)
Space Complexity: O(n) auxiliary space for the sorted copy
"""


def largest_sum_after_k_negations(nums: list[int], k: int) -> int:
    """Return the largest array sum reachable by negating one element, exactly k times."""
    ordered = sorted(nums)
    for i, value in enumerate(ordered):
        if k == 0 or value >= 0:
            break
        ordered[i] = -value
        k -= 1

    total = sum(ordered)
    if k % 2 == 1:
        total -= 2 * min(ordered)
    return total
