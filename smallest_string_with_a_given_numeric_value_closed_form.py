"""
Smallest String With A Given Numeric Value: Closed-Form Construction.

1. Spend the one mandatory point per character, leaving extra = k - n points to distribute.
2. The smallest string pushes all weight to the right: as many 'z's (25 extra each) as possible,
   i.e. z_count = extra // 25.
3. The leftover extra % 25 goes on a single character just left of the z's.
4. Everything before that is 'a'. No loop and no per-character arithmetic: the string is
   assembled from three repeated segments.

Time Complexity: O(n) to build the output string (O(1) arithmetic)
Space Complexity: O(n) for the output
"""


def get_smallest_string(n: int, k: int) -> str:
    """Return the lexicographically smallest string with length n and numeric value k.

    Raises ValueError if no such string exists, i.e. unless n <= k <= 26 * n.
    """
    if not 0 <= n <= k <= 26 * n:
        raise ValueError(f"no string of length {n} has numeric value {k}: need n <= k <= 26 * n")
    if n == 0:
        return ""

    z_count, middle = divmod(k - n, 25)
    if z_count == n:  # k == 26 * n: every character is 'z', no middle character
        return "z" * n
    return "a" * (n - z_count - 1) + chr(ord("a") + middle) + "z" * z_count
