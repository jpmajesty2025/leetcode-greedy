"""
Longest Palindrome by Concatenating Two-Letter Words: Streaming Match Alternative.

1. Walks the words once, keeping a Counter of words still waiting for a mirror partner.
2. If the reverse of the current word is waiting, they pair up: consume it and add 4.
3. Otherwise the word joins the waiting pool.
4. At the end, any waiting palindromic word like "aa" can sit in the center for +2.

Single pass; each word is matched the moment its partner appears.

Time Complexity: O(n)
Space Complexity: O(d) where d is the number of distinct unmatched words (at most 676)
"""

from collections import Counter


def longest_palindrome(words: list[str]) -> int:
    """Return the length of the longest palindrome built from distinct uses of the words."""
    waiting: Counter[str] = Counter()
    length = 0

    for word in words:
        reverse = word[::-1]
        if waiting[reverse] > 0:
            waiting[reverse] -= 1
            length += 4
        else:
            waiting[word] += 1

    has_center = any(n > 0 and word[0] == word[1] for word, n in waiting.items())
    return length + (2 if has_center else 0)
