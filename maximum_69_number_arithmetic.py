"""
Maximum 69 Number: Arithmetic Alternative.

1. Walks the digits from least to most significant using divmod, with no string conversion.
2. Remembers the place value of the most recently seen 6.
3. Because the walk ends at the most significant digit, that is the leftmost 6.
4. Flipping a 6 to a 9 at place value p adds 3 * p.

Time Complexity: O(d) divmod steps, where d is the number of digits
Space Complexity: O(1) auxiliary space
"""


def maximum_69_number(num: int) -> int:
    """Return the largest number reachable by flipping at most one digit of num."""
    leftmost_six_place = 0
    place = 1
    remaining = num
    while remaining:
        remaining, digit = divmod(remaining, 10)
        if digit == 6:
            leftmost_six_place = place
        place *= 10
    return num + 3 * leftmost_six_place
