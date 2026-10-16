"""
Longest Palindrome: Parity-Toggle Alternative.

1. Walks the string once, toggling each character in a set: present means "odd count so far".
2. After the walk, the set holds exactly the characters with an odd total count.
3. Every character contributes all of its copies except one per odd character,
   and one odd character may sit in the middle.
4. Result: len(s) - len(odd) + 1 if any odd character exists, else len(s).

Works for any characters, not only letters. Never builds a frequency table.

Time Complexity: O(n)
Space Complexity: O(k) where k is the number of distinct characters
"""


def longest_palindrome(s: str) -> int:
    """Return the length of the longest palindrome buildable from the characters of s."""
    odd: set[str] = set()
    for ch in s:
        if ch in odd:
            odd.remove(ch)
        else:
            odd.add(ch)
    return len(s) - len(odd) + 1 if odd else len(s)
