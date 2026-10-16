"""
Longest Palindrome: Per-Character str.count Alternative.

1. Takes the distinct characters of the string with set(s).
2. Asks the C-level str.count for each one, so no Python-level loop touches every character.
3. Sums the even part of every count, and adds 1 if any count was odd.

Time Complexity: O(n * k) where k is the number of distinct characters (k <= 52 for letters)
Space Complexity: O(k) auxiliary space
"""


def longest_palindrome(s: str) -> int:
    """Return the length of the longest palindrome buildable from the characters of s."""
    length = 0
    has_odd = False
    for ch in set(s):
        freq = s.count(ch)
        length += freq - (freq & 1)
        has_odd = has_odd or bool(freq & 1)
    return length + has_odd
