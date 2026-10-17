from itertools import permutations

import pytest
from hypothesis import given, settings, strategies as st

import maximum_matching_of_players_with_trainers as orig_module
import maximum_matching_of_players_with_trainers_heaps as heaps_module
import maximum_matching_of_players_with_trainers_sorted as sorted_module


def original(players, trainers):
    """The original sorts its arguments in place, so hand it copies in comparisons."""
    return orig_module.match_players_and_trainers(list(players), list(trainers))


def refactored(players, trainers):
    return sorted_module.match_players_and_trainers(list(players), list(trainers))


def heaps(players, trainers):
    return heaps_module.match_players_and_trainers(list(players), list(trainers))


IMPLS = [original, refactored, heaps]


def brute_force(players: list[int], trainers: list[int]) -> int:
    """Best matching by trying every injective assignment of the smaller side (tiny inputs only)."""
    best = 0
    if len(players) <= len(trainers):
        for order in permutations(range(len(trainers)), len(players)):
            best = max(best, sum(players[p] <= trainers[t] for p, t in enumerate(order)))
    else:
        for order in permutations(range(len(players)), len(trainers)):
            best = max(best, sum(players[p] <= trainers[t] for t, p in enumerate(order)))
    return best


@pytest.mark.parametrize("impl", IMPLS)
@pytest.mark.parametrize(
    "players, trainers, expected",
    [
        ([4, 7, 9], [8, 2, 5, 8], 2),            # LeetCode example 1
        ([1, 1, 1], [10], 1),                    # LeetCode example 2
        ([], [1, 2, 3], 0),                      # no players
        ([1, 2, 3], [], 0),                      # no trainers
        ([], [], 0),
        ([1], [1], 1),                           # exact fit
        ([2], [1], 0),                           # trainer too weak
        ([1, 1, 1], [1, 1, 1], 3),               # everyone matches
        ([5, 5, 5], [4, 4, 4], 0),               # nobody matches
        ([1, 2, 3], [3, 3, 3], 3),               # strong trainers fit all
        ([3, 2, 1], [1, 2, 3], 3),               # unsorted inputs
        ([10, 9, 8, 7], [5, 6, 7, 8], 2),        # only the 7 and 8 trainers qualify
        ([1, 2, 3], [100], 1),                   # one trainer takes only one player
        ([100], [1, 2, 3], 0),                   # weak trainers cannot combine
        ([1, 1, 2, 2], [2, 2], 2),               # trainers go to the weakest players
        ([10**9], [10**9], 1),                   # LeetCode upper bound
        (list(range(1, 30001)), list(range(1, 30001)), 30000),  # LeetCode-scale
    ],
)
def test_known_cases(impl, players, trainers, expected):
    assert impl(players, trainers) == expected


@pytest.mark.parametrize("module", [sorted_module, heaps_module])
def test_does_not_mutate_inputs(module):
    players, trainers = [3, 1, 2], [2, 3, 1]
    module.match_players_and_trainers(players, trainers)
    assert players == [3, 1, 2] and trainers == [2, 3, 1]


@pytest.mark.xfail(
    strict=True,
    reason="Known: players.sort() and trainers.sort() reorder the caller's lists. Remove after switching to sorted().",
)
def test_original_does_not_mutate_inputs():
    players, trainers = [3, 1, 2], [2, 3, 1]
    orig_module.match_players_and_trainers(players, trainers)
    assert players == [3, 1, 2] and trainers == [2, 3, 1]


@pytest.mark.parametrize("impl", IMPLS)
@settings(max_examples=300, deadline=None)
@given(
    players=st.lists(st.integers(min_value=1, max_value=6), max_size=5),
    trainers=st.lists(st.integers(min_value=1, max_value=6), max_size=5),
)
def test_matches_brute_force(impl, players, trainers):
    assert impl(players, trainers) == brute_force(players, trainers)


@settings(max_examples=400, deadline=None)
@given(
    players=st.lists(st.integers(min_value=1, max_value=10**9), max_size=60),
    trainers=st.lists(st.integers(min_value=1, max_value=10**9), max_size=60),
    seed=st.randoms(use_true_random=False),
)
def test_implementations_agree_and_obey_bounds(players, trainers, seed):
    p2, t2 = list(players), list(trainers)
    seed.shuffle(p2)
    seed.shuffle(t2)
    results = {impl(players, trainers) for impl in IMPLS} | {impl(p2, t2) for impl in IMPLS}
    assert len(results) == 1  # all agree and order does not matter
    assert 0 <= results.pop() <= min(len(players), len(trainers))


@settings(max_examples=300, deadline=None)
@given(
    players=st.lists(st.integers(min_value=1, max_value=50), max_size=30),
    trainers=st.lists(st.integers(min_value=1, max_value=50), max_size=30),
    extra=st.integers(min_value=1, max_value=50),
)
def test_monotonic_in_resources(players, trainers, extra):
    base = refactored(players, trainers)
    assert refactored(players, trainers + [extra]) >= base      # an extra trainer never hurts
    assert refactored(players + [extra], trainers) >= base      # an extra player never hurts
    assert refactored(players + [extra], trainers) <= base + 1  # ...and adds at most one match
