"""
Given a string s which consists of lowercase or uppercase letters, return the length of the longest 
palindrome that can be built with those letters.

Letters are case sensitive, for example, "Aa" is not considered a palindrome.
"""

from collections import Counter

def longest_palindrome(s: str) -> int:
    counts = Counter(s).values()
    pairs = sum(c - c % 2 for c in counts)
    return pairs + any(c % 2 for c in counts)