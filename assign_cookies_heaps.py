"""
Assign Cookies: Lazy Two-Heap Alternative.

1. Heapifies copies of the greed factors and cookie sizes in O(n + m); the inputs are untouched.
2. Repeatedly compares the smallest cookie with the least greedy child.
3. A cookie that fits makes that child content (pop both); a cookie that is too small is discarded.
4. Stops the moment either heap is empty.

Time Complexity: O(n + m + k log(n + m)) where k is the number of heap pops actually performed
Space Complexity: O(n + m) auxiliary space
"""

import heapq


def find_content_children(g: list[int], s: list[int]) -> int:
    """Return the maximum number of children that can each receive one big-enough cookie."""
    children = list(g)
    cookies = list(s)
    heapq.heapify(children)
    heapq.heapify(cookies)

    content = 0
    while children and cookies:
        cookie = heapq.heappop(cookies)
        if cookie >= children[0]:
            heapq.heappop(children)
            content += 1
    return content
