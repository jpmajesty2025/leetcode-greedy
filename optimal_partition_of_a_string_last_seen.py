"""
Optimal Partition of a String: Last-Seen Index Alternative.

1. Remember the most recent index of each character, and the start index of the current substring.
2. A repeat exists in the current substring exactly when a character's last index is >= start.
3. In that case, start a new substring at the current index.
4. Nothing is ever cleared: stale entries are simply ignored because they fall before `start`.

Works for any characters, not just lowercase letters, at the cost of a dict that grows with the
alphabet (still O(min(n, alphabet))).

Time Complexity: O(n)
Space Complexity: O(min(n, alphabet size))
"""


def partition_string(s: str) -> int:
    """Return the minimum number of substrings in a partition of s such that the characters in each
    substring are unique.

    An empty string returns 1 (the problem requires one or more substrings).
    """
    last_seen: dict[str, int] = {}
    start = 0
    count = 1
    for index, char in enumerate(s):
        if last_seen.get(char, -1) >= start:
            count += 1
            start = index
        last_seen[char] = index
    return count
