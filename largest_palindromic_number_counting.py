"""
Largest Palindromic Number: Fixed-Size Counting Array.

1. Count the ten digits in a list of ten ints: no sorting and no dictionary.
2. Walk digits 9 down to 0. Each digit contributes count // 2 copies to the left half.
3. The first digit (largest) with a leftover odd copy becomes the centre.
4. An all-zero half would force leading zeros, so it is dropped: the answer becomes the centre
   digit, or "0" if only zeros were available.

Time Complexity: O(n + 10) = O(n)
Space Complexity: O(n) for the output; O(1) auxiliary besides it
"""


def largest_palindromic(num: str) -> str:
    """Return the largest palindromic integer that can be formed using digits taken from num.

    Raises ValueError if num is empty or contains a non-digit character.
    """
    if not num:
        raise ValueError("num must contain at least one digit.")
    if not num.isascii() or not num.isdigit():
        raise ValueError("num must contain only the digits 0-9.")

    counts = [0] * 10
    for char in num:
        counts[ord(char) - ord('0')] += 1

    half = []
    centre = ''
    for digit in range(9, -1, -1):
        if not centre and counts[digit] % 2 == 1:
            centre = str(digit)
        if digit == 0 and not half:
            return centre or '0'  # only zeros are paired: avoid leading zeros
        if counts[digit] >= 2:
            half.append(str(digit) * (counts[digit] // 2))

    left = ''.join(half)
    return left + centre + left[::-1]
