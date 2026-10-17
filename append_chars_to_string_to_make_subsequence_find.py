"""
Append Characters to String to Make Subsequence: str.find Jumping.

1. For each character of t, in order, ask s for its next occurrence at or after the current position.
2. str.find scans in C, so the Python-level loop runs once per character of t, not of s.
3. The first character of t that cannot be found ends the search; everything from there on must be
   appended.

Time Complexity: O(n + m): the find calls together scan s at most once
Space Complexity: O(1)
"""


def append_characters(s: str, t: str) -> int:
    """Return the minimum number of characters to append to s so that t becomes a subsequence of s."""
    position = 0
    for matched, char in enumerate(t):
        found = s.find(char, position)
        if found == -1:
            return len(t) - matched
        position = found + 1
    return 0
