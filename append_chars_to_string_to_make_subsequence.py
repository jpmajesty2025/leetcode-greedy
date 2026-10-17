"""
You are given two strings s and t consisting of only lowercase English letters.

Return the minimum number of characters that need to be appended to the end of s so that t 
becomes a subsequence of s.

A subsequence is a string that can be derived from another string by deleting some or no 
characters without changing the order of the remaining characters.
"""

def append_characters(s: str, t: str) -> int:
    """Return the minimum number of characters that need to be appended to the end of s so that t 
    becomes a subsequence of s.
    """
    matched = 0  # length of the longest prefix of t that is a subsequence of s
    for char in s:
        if matched == len(t):
            break
        if char == t[matched]:
            matched += 1

    return len(t) - matched
