"""
Maximum Ice Cream Bars: Sorted Greedy Alternative.

1. Sorts a copy of the prices ascending, so the caller's list is untouched.
2. Buys bars cheapest first and stops at the first bar the boy cannot afford.
3. Needs no assumptions about the price range, so huge or sparse prices are fine.

Time Complexity: O(n log n)
Space Complexity: O(n) auxiliary space
"""


def max_ice_cream(costs: list[int], coins: int) -> int:
    """Return the maximum number of bars that can be bought with the given coins."""
    bought = 0
    for cost in sorted(costs):
        if cost > coins:
            break
        coins -= cost
        bought += 1
    return bought
