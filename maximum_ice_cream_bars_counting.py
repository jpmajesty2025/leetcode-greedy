"""
Maximum Ice Cream Bars: Refactored Counting Sort.

1. Counts how many bars exist at each price, in a list indexed by price.
2. Walks prices upward and buys a whole price group in one arithmetic step: min(count, coins // price).
3. Stops at the first price group the boy cannot fully afford, since every higher price is worse.
4. Plain module-level function (no stray `self`); never mutates the caller's list.

Precondition: every price is a non-negative integer.

Time Complexity: O(n + C) where C = max(costs), with an early exit once coins run out
Space Complexity: O(C) auxiliary space
"""


def max_ice_cream(costs: list[int], coins: int) -> int:
    """Return the maximum number of bars that can be bought with the given coins."""
    if not costs:
        return 0

    frequency = [0] * (max(costs) + 1)
    for cost in costs:
        frequency[cost] += 1

    bought = 0
    for cost, count in enumerate(frequency):
        if not count:
            continue
        if cost == 0:
            bought += count  # free bars never use coins
            continue
        affordable = min(count, coins // cost)
        bought += affordable
        coins -= affordable * cost
        if affordable < count:
            break
    return bought
