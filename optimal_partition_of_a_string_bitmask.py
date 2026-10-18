"""
Optimal Partition of a String: Bitmask Alternative.

1. Represent the current substring's letters as bits of a single integer (bit 0 = 'a', bit 25 = 'z').
2. If the next letter's bit is already set, close the substring: count it and restart the mask.
3. Otherwise set the bit. No set to clear and no hashing: one AND, one OR per character.

Requires lowercase English letters, as the problem guarantees; any other character raises ValueError.

Time Complexity: O(n)
Space Complexity: O(1): one machine-word-sized integer
"""


def partition_string(s: str) -> int:
    """Return the minimum number of substrings in a partition of s such that the characters in each
    substring are unique.

    An empty string returns 1 (the problem requires one or more substrings).
    """
    count = 1
    mask = 0
    for char in s:
        offset = ord(char) - ord("a")
        if not 0 <= offset < 26:
            raise ValueError(f"expected a lowercase English letter, got {char!r}")
        bit = 1 << offset
        if mask & bit:
            count += 1
            mask = 0
        mask |= bit
    return count
