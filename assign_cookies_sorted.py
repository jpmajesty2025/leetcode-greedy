"""
Assign Cookies: Non-Mutating Two-Pointer Refactor.

1. Sorts copies of the greed factors and cookie sizes, so the caller's lists are untouched.
2. Offers each cookie, smallest first, to the least greedy child still waiting.
3. A cookie that is too small for that child is too small for every remaining child,
   so it is discarded; a cookie that fits makes the child content.
4. Stops as soon as every child is content.

Time Complexity: O(n log n + m log m)
Space Complexity: O(n + m) auxiliary space for the sorted copies
"""


def find_content_children(g: list[int], s: list[int]) -> int:
    """Return the maximum number of children that can each receive one big-enough cookie."""
    greed = sorted(g)
    content = 0
    for cookie in sorted(s):
        if content == len(greed):
            break
        if cookie >= greed[content]:
            content += 1
    return content
