"""
Minimum Addition to Make Integer Beautiful: Quotient Digit Sums.

1. Rounding n up to a multiple of 10**k yields ceil(n / 10**k) followed by k zeros.
2. Trailing zeros add nothing to a digit sum, so the digit sum of the rounded number is just
   the digit sum of ceil(n / 10**k). Compare that against target, no need to build the big number.
3. Try k = 0, 1, 2, ... and return the first rounding that is beautiful.

Time Complexity: O(d^2) in the number of digits d (d candidates, each with an O(d) digit sum)
Space Complexity: O(d)
"""


def make_integer_beautiful(n: int, target: int) -> int:
    """Return the minimum non-negative integer x such that n + x is beautiful.

    Raises ValueError if n < 1 or target < 1.
    """
    if n < 1:
        raise ValueError("n must be at least 1.")
    if target < 1:
        raise ValueError("target must be at least 1.")

    power = 1
    while True:
        quotient = -(-n // power)  # ceil(n / power)
        if sum(map(int, str(quotient))) <= target:
            return quotient * power - n
        power *= 10
