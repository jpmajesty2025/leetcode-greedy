import copy
from functools import lru_cache
from itertools import permutations

import pytest
from hypothesis import given, settings, strategies as st

import earliest_possible_day_of_full_bloom as orig_module
import earliest_possible_day_of_full_bloom_bucket as bucket_module
import earliest_possible_day_of_full_bloom_grouped as grouped_module

IMPLS = [
    orig_module.earliest_full_bloom,
    grouped_module.earliest_full_bloom,
    bucket_module.earliest_full_bloom,
]


def order_cost(plant, grow, order) -> int:
    day = bloom = 0
    for i in order:
        day += plant[i]
        bloom = max(bloom, day + grow[i])
    return bloom


def brute_force_orders(plant, grow) -> int:
    """Best bloom day over every order of planting each seed in one uninterrupted stretch."""
    return min(order_cost(plant, grow, o) for o in permutations(range(len(plant))))


def brute_force_day_by_day(plant, grow) -> int:
    """Best bloom day over every possible day-by-day schedule, including interleaving seeds."""

    @lru_cache(maxsize=None)
    def best(remaining: tuple, finished: tuple, day: int) -> int:
        if all(r == 0 for r in remaining):
            return max(f + g for f, g in zip(finished, grow))
        result = sum(plant) + sum(grow) + 1  # larger than any real schedule's bloom day
        for i, r in enumerate(remaining):
            if r > 0:
                new_remaining = remaining[:i] + (r - 1,) + remaining[i + 1:]
                new_finished = finished[:i] + (day + 1,) + finished[i + 1:] if r == 1 else finished
                result = min(result, best(new_remaining, new_finished, day + 1))
        return result

    # Seeds with plant time 0 are "finished" on day 0; others get their day set when completed.
    finished = tuple(0 for _ in plant)
    return best(tuple(plant), finished, 0)


@pytest.mark.parametrize("impl", IMPLS)
@pytest.mark.parametrize(
    "plant, grow, expected",
    [
        ([1, 4, 3], [2, 3, 1], 9),                  # LeetCode example 1
        ([1, 2, 3, 2], [2, 1, 2, 1], 9),            # LeetCode example 2
        ([1], [1], 2),                              # LeetCode example 3
        ([0], [0], 0),                              # nothing takes any time
        ([5], [0], 5),                              # planting only
        ([0], [5], 5),                              # growing only
        ([2, 2], [3, 3], 7),                        # equal grow times: order irrelevant
        ([1, 1, 1], [3, 2, 1], 4),                  # already in best order
        ([3, 1], [1, 5], 6),                        # slow grower first beats fast planter first
        ([0, 0, 0], [4, 7, 1], 7),                  # free planting: slowest grower decides
        ([4, 4, 4], [0, 0, 0], 12),                 # no growth: total planting time
    ],
)
def test_known_cases(impl, plant, grow, expected):
    assert impl(plant, grow) == expected


@pytest.mark.parametrize("impl", IMPLS)
def test_inputs_are_not_modified(impl):
    plant, grow = [1, 4, 3], [2, 3, 1]
    snapshot = copy.deepcopy((plant, grow))
    impl(plant, grow)
    assert (plant, grow) == snapshot


@pytest.mark.parametrize("impl", IMPLS)
@pytest.mark.parametrize(
    "plant, grow",
    [
        ([1, 2], [1]),         # length mismatch
        ([1], [1, 2]),
        ([], []),              # empty
        ([-1], [2]),           # negative plant time
        ([2], [-5]),           # negative grow time
        ([1, -1], [1, 1]),
    ],
)
def test_invalid_input_raises(impl, plant, grow):
    with pytest.raises(ValueError):
        impl(plant, grow)


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_scale(impl):
    n = 100_000
    plant = [1] * n
    grow = [i % 10_000 for i in range(n)]
    assert impl(plant, grow) == orig_module.earliest_full_bloom(plant, grow)
    # all seeds identical: plant them back to back, last one blooms after one growth period
    assert impl([3] * n, [7] * n) == 3 * n + 7


@pytest.mark.parametrize("impl", IMPLS)
@settings(max_examples=300, deadline=None)
@given(
    seeds=st.lists(st.tuples(st.integers(0, 6), st.integers(0, 6)), min_size=1, max_size=6),
)
def test_matches_brute_force_over_all_orders(impl, seeds):
    plant, grow = [s[0] for s in seeds], [s[1] for s in seeds]
    assert impl(plant, grow) == brute_force_orders(plant, grow)


@pytest.mark.parametrize("impl", IMPLS)
@settings(max_examples=100, deadline=None)
@given(
    seeds=st.lists(st.tuples(st.integers(0, 3), st.integers(0, 5)), min_size=1, max_size=3),
)
def test_interleaving_planting_never_beats_the_greedy(impl, seeds):
    """The problem allows splitting a seed's planting across days; check that never helps."""
    plant, grow = [s[0] for s in seeds], [s[1] for s in seeds]
    assert impl(plant, grow) == brute_force_day_by_day(plant, grow)


@settings(max_examples=500, deadline=None)
@given(
    seeds=st.lists(st.tuples(st.integers(0, 50), st.integers(0, 50)), min_size=1, max_size=200),
)
def test_implementations_agree_and_obey_bounds(seeds):
    plant, grow = [s[0] for s in seeds], [s[1] for s in seeds]
    results = {impl(plant, grow) for impl in IMPLS}
    assert len(results) == 1
    result = results.pop()
    assert result >= sum(plant)                          # all planting must happen
    assert result >= max(p + g for p, g in seeds)        # every seed needs its own plant + grow time
    assert result <= sum(plant) + max(grow)              # worst case: wait for the slowest at the end


@settings(max_examples=300, deadline=None)
@given(
    seeds=st.lists(st.tuples(st.integers(0, 30), st.integers(0, 30)), min_size=1, max_size=40),
    seed=st.randoms(use_true_random=False),
)
def test_input_order_is_irrelevant(seeds, seed):
    shuffled = list(seeds)
    seed.shuffle(shuffled)
    a = orig_module.earliest_full_bloom([s[0] for s in seeds], [s[1] for s in seeds])
    b = orig_module.earliest_full_bloom([s[0] for s in shuffled], [s[1] for s in shuffled])
    assert a == b


@settings(max_examples=300, deadline=None)
@given(
    seeds=st.lists(st.tuples(st.integers(0, 30), st.integers(0, 30)), min_size=1, max_size=30),
    extra=st.integers(1, 10),
)
def test_slower_planting_or_growing_never_helps(seeds, extra):
    plant, grow = [s[0] for s in seeds], [s[1] for s in seeds]
    base = orig_module.earliest_full_bloom(plant, grow)
    assert orig_module.earliest_full_bloom([plant[0] + extra] + plant[1:], grow) >= base
    assert orig_module.earliest_full_bloom(plant, [grow[0] + extra] + grow[1:]) >= base
