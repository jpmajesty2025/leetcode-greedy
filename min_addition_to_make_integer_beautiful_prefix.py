"""
Minimum Addition to Make Integer Beautiful: Longest Safe Prefix.

1. If n is already beautiful, the answer is 0.
2. Otherwise keep the longest prefix of n's digits whose sum is at most target - 1.
3. Increment that prefix by one and replace every remaining digit with 0.

Why it works: adding 1 to a prefix raises its digit sum by at most 1 (carries only lower it), so the
result has digit sum <= target. A longer prefix would already exceed target - 1, and any carry that
rescues it just lands on a number made from a shorter safe prefix, which we already consider.
An empty prefix gives 10**len(n), whose digit sum is 1.

Works directly on the digit string: no repeated digit-sum recomputation.

Time Complexity: O(d), where d is the number of digits of n
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

    digits = str(n)
    if sum(map(int, digits)) <= target:
        return 0

    prefix_sum = 0
    keep = 0  # number of leading digits we keep
    while keep < len(digits) and prefix_sum + int(digits[keep]) <= target - 1:
        prefix_sum += int(digits[keep])
        keep += 1

    prefix = int(digits[:keep]) if keep else 0
    rounded = (prefix + 1) * 10 ** (len(digits) - keep)
    return rounded - n
