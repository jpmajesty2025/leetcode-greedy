"""
Longest Palindrome by Concatenating Two-Letter Words: Fixed Counter Version.

1. Counts each word with collections.Counter.
2. A word like "aa" pairs with itself: floor(freq / 2) pairs, and one leftover can be the center.
3. A word like "ab" pairs with its reverse "ba": min(freq, freq of reverse) pairs.
   Each unordered pair of mirror words is handled exactly once (when word < reverse),
   so nothing is double counted and the Counter is never mutated.
4. Each pair of words adds 4 letters; a center word adds 2.

Time Complexity: O(n)
Space Complexity: O(d) where d is the number of distinct words (at most 676)
"""

from collections import Counter


def longest_palindrome(words: list[str]) -> int:
    """Return the length of the longest palindrome built from distinct uses of the words."""
    count = Counter(words)
    length = 0
    has_center = False

    for word, freq in count.items():
        reverse = word[::-1]
        if word == reverse:
            length += (freq // 2) * 4
            has_center = has_center or freq % 2 == 1
        elif word < reverse:
            length += min(freq, count.get(reverse, 0)) * 4

    return length + (2 if has_center else 0)
