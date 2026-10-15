"""
Maximum Units on a Truck: Bucket Alternative.

1. Sums the number of boxes available at each units-per-box value into a list indexed by that value.
2. Scans the buckets from the highest units-per-box down to 1, loading boxes until the truck is full.
3. Never mutates the caller's list.

Time Complexity: O(n + U) where U = max units per box
Space Complexity: O(U) auxiliary space
"""


def maximum_units(boxTypes: list[list[int]], truckSize: int) -> int:
    """Return the maximum total units that fit on a truck holding truckSize boxes."""
    if not boxTypes or truckSize <= 0:
        return 0

    buckets = [0] * (max(units for _, units in boxTypes) + 1)
    for boxes, units in boxTypes:
        buckets[units] += boxes

    total_units = 0
    for units in range(len(buckets) - 1, 0, -1):
        if truckSize == 0:
            break
        take = min(buckets[units], truckSize)
        total_units += take * units
        truckSize -= take
    return total_units
