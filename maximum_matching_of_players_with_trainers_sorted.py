"""
Maximum Matching of Players With Trainers: Non-Mutating Two-Pointer Refactor.

1. Sorts copies of the player abilities and trainer capacities, so the caller's lists are untouched.
2. Offers each trainer, weakest first, to the weakest player still waiting.
3. A trainer who cannot handle that player cannot handle any remaining player, so is skipped;
   a trainer who can makes a match.
4. Stops as soon as every player is matched.

Time Complexity: O(n log n + m log m)
Space Complexity: O(n + m) auxiliary space for the sorted copies
"""


def match_players_and_trainers(players: list[int], trainers: list[int]) -> int:
    """Return the maximum number of players that can each be matched to a distinct capable trainer."""
    abilities = sorted(players)
    matches = 0
    for capacity in sorted(trainers):
        if matches == len(abilities):
            break
        if abilities[matches] <= capacity:
            matches += 1
    return matches
