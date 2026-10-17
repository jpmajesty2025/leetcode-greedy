"""
Maximum Matching of Players With Trainers: Lazy Two-Heap Alternative.

1. Heapifies copies of the player abilities and trainer capacities in O(n + m); inputs are untouched.
2. Repeatedly pops the weakest trainer and compares it with the weakest waiting player.
3. If the trainer can handle that player, pop the player too and count a match; otherwise the
   trainer is discarded.
4. Stops the moment either heap is empty, so unused tails are never ordered.

Time Complexity: O(n + m + k log(n + m)) where k is the number of heap pops actually performed
Space Complexity: O(n + m) auxiliary space
"""

import heapq


def match_players_and_trainers(players: list[int], trainers: list[int]) -> int:
    """Return the maximum number of players that can each be matched to a distinct capable trainer."""
    waiting = list(players)
    available = list(trainers)
    heapq.heapify(waiting)
    heapq.heapify(available)

    matches = 0
    while waiting and available:
        capacity = heapq.heappop(available)
        if waiting[0] <= capacity:
            heapq.heappop(waiting)
            matches += 1
    return matches
