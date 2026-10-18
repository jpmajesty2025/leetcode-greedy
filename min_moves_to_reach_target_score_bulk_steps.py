"""
Minimum Moves to Reach Target Score: Divide-and-Subtract Loop (Bulk Steps).

A variant of the backward greedy that handles each halving in one step instead of two:
1. While doubles remain and target > 1: an odd target costs one decrement, then the halving costs
   one more, so add 1 + (target % 2) and replace target with target // 2.
2. Once doubles run out (or target reaches 1), the rest is target - 1 increments.

Same answers as the classic greedy, with at most about log2(target) loop iterations in every case.

Time Complexity: O(log target)
Space Complexity: O(1)
"""


def min_moves(target: int, maxDoubles: int) -> int:
    """Return the minimum number of moves needed to reach target starting with 1.

    Raises ValueError if target < 1 (unreachable from 1) or maxDoubles < 0.
    """
    if target < 1:
        raise ValueError("target must be at least 1.")
    if maxDoubles < 0:
        raise ValueError("maxDoubles must be non-negative.")

    moves = 0
    while maxDoubles > 0 and target > 1:
        moves += 1 + (target % 2)  # optional decrement, then the halving
        target //= 2
        maxDoubles -= 1
    return moves + target - 1
