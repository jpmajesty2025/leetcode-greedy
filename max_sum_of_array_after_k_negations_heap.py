"""
Maximize Sum After K Negations: Min-Heap Simulation.

1. Heapifies a copy of the numbers in O(n).
2. k times: pop the smallest value, negate it, and push it back.
   The smallest value is always the best one to negate:
   a negative number becomes positive, and once everything is non-negative,
   the smallest one costs the least to flip.
3. Returns the sum.

Handles any k: once the negatives are gone, each pair of extra flips cancels,
so the loop exits after at most one more flip (only k % 2 matters).

Time Complexity: O(n + (min(k, negatives) + 1) * log n)
Space Complexity: O(n) auxiliary space for the heap
"""

import heapq


def largest_sum_after_k_negations(nums: list[int], k: int) -> int:
    """Return the largest array sum reachable by negating one element, exactly k times."""
    heap = list(nums)
    heapq.heapify(heap)

    while k > 0:
        smallest = heap[0]
        if smallest >= 0:
            # Every value is non-negative: flips cancel in pairs, so only parity is left.
            if k % 2 == 1:
                heapq.heapreplace(heap, -smallest)
            break
        heapq.heapreplace(heap, -smallest)
        k -= 1

    return sum(heap)
