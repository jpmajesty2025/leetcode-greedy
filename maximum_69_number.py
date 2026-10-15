"""
You are given a positive integer num consisting only of digits 6 and 9.

Return the maximum number you can get by changing at most one digit (6 becomes 9, and 9 becomes 6).
"""

def maximum_69_number (num: int) -> int:
    num_str = str(num)
    max_num_str = num_str.replace('6', '9', 1)
    return int(max_num_str)