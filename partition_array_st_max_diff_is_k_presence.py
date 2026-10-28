"""
Partition Array Such That Maximum Difference Is K: Presence-Array Alternative.

1. Marks which values occur in a boolean array indexed by (value - min), in O(n).
2. Scans the value range once, left to right. Duplicates need no special handling.
3. Starts a new group whenever a present value is more than k above the group's smallest value.
4. Never mutates the caller's list.

Time Complexity: O(n + R) where R = max(nums) - min(nums) + 1
Space Complexity: O(R) auxiliary space
"""


def partition_array(nums: list[int], k: int) -> int:
    """Return the minimum number of groups so that max - min <= k within each group."""
    if not nums:
        return 0

    low = min(nums)
    present = bytearray(max(nums) - low + 1)
    for num in nums:
        present[num - low] = 1

    groups = 0
    group_start = -k - 1  # offset guaranteed to be more than k below index 0
    for offset, seen in enumerate(present):
        if seen and offset - group_start > k:
            groups += 1
            group_start = offset
    return groups
