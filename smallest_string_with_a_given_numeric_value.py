"""
The numeric value of a lowercase character is defined as its position (1-indexed) in the alphabet, 
so the numeric value of a is 1, the numeric value of b is 2, the numeric value of c is 3, and so on.

The numeric value of a string consisting of lowercase characters is defined as the sum of its 
characters' numeric values. For example, the numeric value of the string "abe" is equal to 
1 + 2 + 5 = 8.

You are given two integers n and k. Return the lexicographically smallest string with length equal 
to n and numeric value equal to k.

Note that a string x is lexicographically smaller than string y if x comes before y in dictionary 
order, that is, either x is a prefix of y, or if i is the first position such that x[i] != y[i], 
then x[i] comes before y[i] in alphabetic order.
"""

def get_smallest_string(n: int, k: int) -> str:
    """Return the lexicographically smallest string with length equal to n and numeric value equal to k.

    Raises ValueError if no such string exists, i.e. unless n <= k <= 26 * n.
    """
    if not 0 <= n <= k <= 26 * n:
        raise ValueError(f"no string of length {n} has numeric value {k}: need n <= k <= 26 * n")

    # Initialize a list of 'a's of length n
    result = ['a'] * n
    # Calculate the remaining value after filling with 'a's
    remaining_value = k - n

    # Start from the end of the string and fill in the characters
    index = n - 1
    while remaining_value > 0:
        # Determine the maximum value we can place at this position
        add_value = min(25, remaining_value)  # 'z' is 26, 'a' is 1, so max we can add is 25
        result[index] = chr(ord('a') + add_value)  # Convert to character
        remaining_value -= add_value
        index -= 1

    return ''.join(result)
