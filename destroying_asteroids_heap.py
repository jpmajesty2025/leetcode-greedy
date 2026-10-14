"""
Destroying Asteroids: Lazy Min-Heap Alternative.

1. Copies the asteroids and heapifies the copy in O(n); the caller's list is untouched.
2. Repeatedly pops the lightest remaining asteroid.
3. Stops the moment the planet cannot beat the lightest one left.
4. Stops early with True once the planet outweighs the heaviest asteroid.

Time Complexity: O(n + m log n) where m is the number of asteroids actually popped
Space Complexity: O(n) auxiliary space
"""

import heapq


def asteroids_destroyed(mass: int, asteroids: list[int]) -> bool:
    """Return True if the planet can destroy every asteroid, popping lazily from a heap."""
    heap = list(asteroids)
    heapq.heapify(heap)
    ceiling = max(heap, default=0)

    while heap:
        if mass >= ceiling:
            return True
        lightest = heapq.heappop(heap)
        if mass < lightest:
            return False
        mass += lightest
    return True
