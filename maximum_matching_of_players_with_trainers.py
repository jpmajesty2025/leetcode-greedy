"""
You are given a 0-indexed integer array players, where players[i] represents the ability of the 
ith player. You are also given a 0-indexed integer array trainers, where trainers[j] represents 
the training capacity of the jth trainer.

The ith player can match with the jth trainer if the player's ability is less than or equal to the 
trainer's training capacity. Additionally, the ith player can be matched with at most one trainer, 
and the jth trainer can be matched with at most one player.

Return the maximum number of matchings between players and trainers that satisfy these conditions.
"""

def match_players_and_trainers(players: list[int], trainers: list[int]) -> int:
    """Return the maximum number of matchings between players and trainers."""
    players.sort()
    trainers.sort()

    player_index = 0
    trainer_index = 0
    matches = 0

    while player_index < len(players) and trainer_index < len(trainers):
        if players[player_index] <= trainers[trainer_index]:
            matches += 1
            player_index += 1
            trainer_index += 1
        else:
            trainer_index += 1

    return matches