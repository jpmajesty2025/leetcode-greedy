"""
You are given two positive integers n and target.

An integer is considered beautiful if the sum of its digits is less than or equal to target.

Return the minimum non-negative integer x such that n + x is beautiful. The input will be generated such 
that it is always possible to make n beautiful.
"""

def make_integer_beautiful(n: int, target: int) -> int:
    """Return the minimum non-negative integer x such that n + x is beautiful.

    An integer is considered beautiful if the sum of its digits is less than or equal to target.

    Raises ValueError if n < 1 or target < 1 (target < 1 would make some inputs impossible, since every
    positive integer has digit sum at least 1).
    """
    if n < 1:
        raise ValueError("n must be at least 1.")
    if target < 1:
        raise ValueError("target must be at least 1.")

    def digit_sum(num: int) -> int:
        """Return the sum of the digits of num."""
        return sum(int(digit) for digit in str(num))

    # The cheapest way to shrink a digit sum is to round n up to the next multiple of 10, then 100,
    # then 1000, ...: each rounding zeroes more trailing digits. The first rounding that is beautiful
    # is the answer. Rounding up to 10**len(n) always works, since its digit sum is 1.
    value = n
    power = 1
    while digit_sum(value) > target:
        power *= 10
        value = -(-value // power) * power  # ceil to a multiple of power
    return value - n
