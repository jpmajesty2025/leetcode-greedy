"""
Largest Palindromic Number: Sorted Pairing Scan.

1. Sort the digits descending, so equal digits sit next to each other and big digits come first.
2. Scan once: whenever two neighbours are equal, they form a pair for the palindrome; consume both.
   Otherwise the lone digit is a centre candidate, and the first (largest) candidate wins.
3. Pairs are collected in descending order, which is exactly the best left half.
4. An all-zero half is dropped to avoid leading zeros: answer is the centre, or "0".

A different view of the same greedy: pairs found by adjacency instead of by counting.

Time Complexity: O(n log n) for the sort
Space Complexity: O(n)
"""


def largest_palindromic(num: str) -> str:
    """Return the largest palindromic integer that can be formed using digits taken from num.

    Raises ValueError if num is empty or contains a non-digit character.
    """
    if not num:
        raise ValueError("num must contain at least one digit.")
    if not num.isascii() or not num.isdigit():
        raise ValueError("num must contain only the digits 0-9.")

    digits = sorted(num, reverse=True)
    pairs = []
    centre = ''
    i = 0
    while i < len(digits):
        if i + 1 < len(digits) and digits[i] == digits[i + 1]:
            pairs.append(digits[i])
            i += 2
        else:
            if not centre:
                centre = digits[i]
            i += 1

    if not pairs or pairs[0] == '0':
        return centre or '0'
    left = ''.join(pairs)
    return left + centre + left[::-1]
