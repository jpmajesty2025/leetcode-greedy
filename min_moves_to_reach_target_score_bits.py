"""
Minimum Moves to Reach Target Score: Bit-Counting Closed Form.

Working backwards from target, each halving costs 1 move, plus 1 more if the value is odd (a
decrement first). Halving d times therefore costs d plus the number of 1-bits among the low d bits
of target, and leaves r = target >> d, which then costs r - 1 increments to reach 1.

1. d = min(maxDoubles, target.bit_length() - 1): more doubles than that would go below 1.
2. moves = d + popcount(target's low d bits) + ((target >> d) - 1).

No loop at all.

Time Complexity: O(log target) for the bit operations (effectively O(1) for machine-size ints)
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

    doubles = min(maxDoubles, target.bit_length() - 1)
    low_bits = target & ((1 << doubles) - 1)
    return doubles + bin(low_bits).count("1") + (target >> doubles) - 1
