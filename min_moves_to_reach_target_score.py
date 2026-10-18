"""
You are playing a game with integers. You start with the integer 1 and you want to reach the integer target.

In one move, you can either:

Increment the current integer by one (i.e., x = x + 1).
Double the current integer (i.e., x = 2 * x).
You can use the increment operation any number of times, however, you can only use the double operation 
at most maxDoubles times.

Given the two integers target and maxDoubles, return the minimum number of moves needed to reach target 
starting with 1.
"""

def min_moves(target: int, maxDoubles: int) -> int:
    """Return the minimum number of moves needed to reach target starting with 1.

    In one move, you can either increment the current integer by one or double the current integer.
    You can use the increment operation any number of times, however, you can only use the double 
    operation at most maxDoubles times.

    Raises ValueError if target < 1 (unreachable from 1) or maxDoubles < 0.
    """
    if target < 1:
        raise ValueError("target must be at least 1.")
    if maxDoubles < 0:
        raise ValueError("maxDoubles must be non-negative.")

    moves = 0
    while target > 1:
        if maxDoubles == 0:
            # No doubles left: only increments remain, so jump straight to 1 instead of looping
            # target - 1 times (up to ~10^9 iterations).
            return moves + target - 1
        if target % 2 == 0:
            target //= 2
            maxDoubles -= 1
        else:
            target -= 1
        moves += 1
    return moves
