"""
Smallest String With A Given Numeric Value: Forward Greedy (Feasibility Check).

1. Build the string left to right, since lexicographic order is decided by the earliest position.
2. At each position, pick the smallest letter such that the remaining positions can still reach
   the remaining value: after placing value v, we need rest - v <= 26 * (positions left).
3. That gives v = max(1, rest - 26 * positions_left); the choice never needs backtracking.

This is the textbook "smallest first" greedy, and reads directly like the problem statement.

Time Complexity: O(n)
Space Complexity: O(n) for the output
"""


def get_smallest_string(n: int, k: int) -> str:
    """Return the lexicographically smallest string with length n and numeric value k.

    Raises ValueError if no such string exists, i.e. unless n <= k <= 26 * n.
    """
    if not 0 <= n <= k <= 26 * n:
        raise ValueError(f"no string of length {n} has numeric value {k}: need n <= k <= 26 * n")

    chars = []
    remaining = k
    for positions_left in range(n - 1, -1, -1):
        value = max(1, remaining - 26 * positions_left)
        chars.append(chr(ord("a") + value - 1))
        remaining -= value
    return "".join(chars)
