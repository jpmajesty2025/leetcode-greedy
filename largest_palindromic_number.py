"""
You are given a string num consisting of digits only.

Return the largest palindromic integer (in the form of a string) that can be formed using digits taken 
from num. It should not contain leading zeroes.

Notes:

You do not need to use all the digits of num, but you must use at least one digit.
The digits can be reordered.
"""

from collections import Counter


def largest_palindromic(num: str) -> str:
    """Return the largest palindromic integer that can be formed using digits taken from num.

    A palindrome made only of zeros collapses to "0", the only integer allowed to start with 0.

    Raises ValueError if num is empty or contains a non-digit character.
    """
    if not num:
        raise ValueError("num must contain at least one digit.")
    if not num.isascii() or not num.isdigit():
        raise ValueError("num must contain only the digits 0-9.")

    # Count the frequency of each digit
    digit_count = Counter(num)

    # Build the left half from the largest digit down; remember the largest digit left over (odd count)
    half_palindrome = []
    middle_digit = ''
    for digit in sorted(digit_count, reverse=True):
        count = digit_count[digit]
        if count % 2 == 1 and not middle_digit:  # first odd digit seen is the largest
            middle_digit = digit
        half_palindrome.append(digit * (count // 2))
    half = ''.join(half_palindrome)

    # The half is sorted descending, so it starts with '0' only if it is all zeros.
    # Padding a palindrome with zeros would create leading zeros, so drop them entirely.
    if half and half[0] == '0':
        return middle_digit or '0'

    return half + middle_digit + half[::-1]
