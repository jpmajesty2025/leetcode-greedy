"""
Maximum Number of Apples in a Basket: Bucket Alternative.

1. Counts how many apples have each weight in a list indexed by weight.
2. Scans weights from lightest to heaviest, taking as many apples of that weight as still fit.
3. Stops at the first weight that does not fit completely, since every heavier one fits even less.
4. Never mutates the caller's list. Capacity is a parameter instead of a magic number.

Precondition: every weight is a positive integer.

Time Complexity: O(n + W) where W = max(weight)
Space Complexity: O(W) auxiliary space
"""

BASKET_CAPACITY = 5000


def max_number_of_apples(weight: list[int], capacity: int = BASKET_CAPACITY) -> int:
    """Return the maximum number of apples whose total weight is at most capacity."""
    if not weight or capacity <= 0:
        return 0

    buckets = [0] * (max(weight) + 1)
    for w in weight:
        buckets[w] += 1

    count = 0
    remaining = capacity
    for w in range(1, len(buckets)):
        if not buckets[w]:
            continue
        take = min(buckets[w], remaining // w)
        count += take
        remaining -= take * w
        if take < buckets[w]:
            break
    return count
