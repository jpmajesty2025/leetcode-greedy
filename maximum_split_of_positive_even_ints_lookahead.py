"""
Maximum Split of Positive Even Integers: Look-Ahead Greedy (No Fix-Up Step).

1. Keep the remaining sum and the next candidate even number.
2. Take the candidate only if the rest can still be made of strictly larger numbers: either nothing
   is left over, or what remains is bigger than the candidate (so it can go on as one bigger piece).
3. Otherwise the remaining sum itself becomes the final element and we stop.

This folds the "add the leftover to the last element" correction into the loop: every element is
decided once and never edited afterwards.

Time Complexity: O(sqrt(finalSum))
Space Complexity: O(sqrt(finalSum)) for the output
"""


def maximum_even_split(finalSum: int) -> list[int]:
    """Return a list of unique positive even integers that sum up to finalSum.

    If no valid split exists for finalSum (it is odd, zero or negative), return an empty list.
    """
    if finalSum % 2 != 0 or finalSum <= 0:
        return []

    result = []
    remaining = finalSum
    candidate = 2
    while remaining > 0:
        if remaining - candidate == 0 or remaining - candidate > candidate:
            result.append(candidate)
            remaining -= candidate
            candidate += 2
        else:
            result.append(remaining)  # too little left to place another distinct number after this
            break
    return result
