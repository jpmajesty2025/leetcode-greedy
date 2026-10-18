"""
Minimum Number of Taps to Open to Water a Garden: Dynamic Programming.

1. dp[j] = the minimum number of taps needed to water [0, j]; dp[0] = 0, everything else unreachable.
2. For each tap with clamped interval [left, right], every point j in (left, right] can be finished
   by this tap once [0, left] is watered: dp[j] = min(dp[j], dp[left] + 1).
3. dp[n] is the answer, or -1 if still unreachable.

Slower than the greedy versions, but it is a direct recurrence with no greedy argument, so it is a
good independent cross-check.

Time Complexity: O(n * max range): each tap updates the points it covers
Space Complexity: O(n)
"""


def min_taps(n: int, ranges: list[int]) -> int:
    """Return the minimum number of taps that should be open to water the whole garden.

    If the garden cannot be watered return -1. The input is not modified.

    Raises ValueError if n is negative, if ranges does not have length n + 1,
    or if any range is negative.
    """
    if n < 0:
        raise ValueError("n must be non-negative.")
    if len(ranges) != n + 1:
        raise ValueError("ranges must have length n + 1.")
    if min(ranges) < 0:
        raise ValueError("ranges must not contain negative values.")

    # Integer sentinel: a minimal solution opens each tap at most once, so n + 2 is never a real answer
    unreachable = n + 2
    dp: list[int] = [unreachable] * (n + 1)
    dp[0] = 0
    # Process taps in order of their left end so dp[left] is final before it is used
    taps = sorted((max(0, i - r), min(n, i + r)) for i, r in enumerate(ranges))
    for left, right in taps:
        if dp[left] == unreachable:
            continue
        for j in range(left + 1, right + 1):
            if dp[left] + 1 < dp[j]:
                dp[j] = dp[left] + 1
    return -1 if dp[n] == unreachable else dp[n]
