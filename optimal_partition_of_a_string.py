"""
Given a string s, partition the string into one or more substrings such that the characters in each 
substring are unique. That is, no letter appears in a single substring more than once.

Return the minimum number of substrings in such a partition.

Note that each character should belong to exactly one substring in a partition.
"""

def partition_string(s: str) -> int:
    """Return the minimum number of substrings in a partition of s such that the characters in each 
    substring are unique.

    An empty string returns 1 (the problem requires one or more substrings; LeetCode guarantees len(s) >= 1).
    """
    seen = set()  # to track characters in the current substring
    count = 1  # at least one substring is needed

    for char in s:
        if char in seen:
            # If the character is already seen, we need to start a new substring
            count += 1
            seen.clear()  # reset for the new substring
        seen.add(char)  # add the character to the current substring

    return count
