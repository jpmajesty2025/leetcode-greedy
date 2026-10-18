import time
from collections import deque

import pytest
from hypothesis import given, settings, strategies as st

import min_moves_to_reach_target_score as orig_module
import min_moves_to_reach_target_score_bits as bits_module
import min_moves_to_reach_target_score_bulk_steps as bulk_module

IMPLS = [
    orig_module.min_moves,
    bits_module.min_moves,
    bulk_module.min_moves,
]


def bfs_oracle(target: int, max_doubles: int) -> int:
    """Forward breadth-first search over (value, doubles used); exact for small targets."""
    start = (1, 0)
    seen = {start}
    queue = deque([(start, 0)])
    while queue:
        (value, used), dist = queue.popleft()
        if value == target:
            return dist
        nxt = [(value + 1, used)]
        if used < max_doubles:
            nxt.append((value * 2, used + 1))
        for state in nxt:
            if state[0] <= target and state not in seen:
                seen.add(state)
                queue.append((state, dist + 1))
    raise AssertionError("target is always reachable by increments")


@pytest.mark.parametrize("impl", IMPLS)
@pytest.mark.parametrize(
    "target, max_doubles, expected",
    [
        (5, 0, 4),                # LeetCode example 1: only increments
        (19, 2, 7),               # LeetCode example 2
        (10, 4, 4),               # LeetCode example 3
        (1, 0, 0),                # already there
        (1, 5, 0),                # doubles never help at 1
        (2, 0, 1),
        (2, 1, 1),                # +1 and *2 both take one move
        (3, 1, 2),                # 1 -> 2 (double) -> 3
        (4, 1, 2),                # 1 -> 2 -> 4
        (7, 100, 4),              # 1 -> 2 -> 3 -> 6 -> 7; extra doubles are unused
        (8, 3, 3),                # pure doubling
        (1000, 0, 999),
        (15, 1, 8),               # one double is worth little
        (16, 4, 4),
    ],
)
def test_known_cases(impl, target, max_doubles, expected):
    assert impl(target, max_doubles) == expected


@pytest.mark.parametrize("impl", IMPLS)
@pytest.mark.parametrize(
    "target, max_doubles",
    [(0, 0), (-1, 3), (-100, 0), (0, 5)],
)
def test_unreachable_target_raises(impl, target, max_doubles):
    with pytest.raises(ValueError):
        impl(target, max_doubles)


@pytest.mark.parametrize("impl", IMPLS)
@pytest.mark.parametrize("max_doubles", [-1, -10])
def test_negative_doubles_raise(impl, max_doubles):
    with pytest.raises(ValueError):
        impl(10, max_doubles)


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_limits_are_fast(impl):
    """Regression: with maxDoubles == 0 the original looped target - 1 times (about a minute at 10**9)."""
    start = time.perf_counter()
    assert impl(10**9, 0) == 10**9 - 1
    assert impl(10**9, 100) == impl(10**9, 30)  # doubles beyond bit_length are never used
    assert impl(10**9, 1) > 0
    assert time.perf_counter() - start < 1.0


@pytest.mark.parametrize("impl", IMPLS)
@settings(max_examples=300, deadline=None)
@given(target=st.integers(min_value=1, max_value=80), max_doubles=st.integers(min_value=0, max_value=8))
def test_matches_bfs_oracle(impl, target, max_doubles):
    assert impl(target, max_doubles) == bfs_oracle(target, max_doubles)


@settings(max_examples=1000, deadline=None)
@given(target=st.integers(min_value=1, max_value=10**9), max_doubles=st.integers(min_value=0, max_value=100))
def test_implementations_agree_and_obey_bounds(target, max_doubles):
    results = {impl(target, max_doubles) for impl in IMPLS}
    assert len(results) == 1
    moves = results.pop()
    assert 0 <= moves <= target - 1  # increments alone always work
    # every move at most doubles the value, so reaching target needs at least log2(target) moves
    assert moves >= target.bit_length() - 1


@settings(max_examples=300, deadline=None)
@given(target=st.integers(min_value=1, max_value=10**6), max_doubles=st.integers(min_value=0, max_value=25))
def test_more_doubles_never_hurt(target, max_doubles):
    assert bits_module.min_moves(target, max_doubles + 1) <= bits_module.min_moves(target, max_doubles)


@settings(max_examples=300, deadline=None)
@given(target=st.integers(min_value=1, max_value=10**6), max_doubles=st.integers(min_value=0, max_value=25))
def test_next_target_costs_at_most_one_more_move(target, max_doubles):
    """Not monotone (7 costs 4 but 8 costs 3 with two doubles), but one extra increment always works."""
    assert bits_module.min_moves(target + 1, max_doubles) <= bits_module.min_moves(target, max_doubles) + 1


def test_cost_is_not_monotone_in_target():
    assert bits_module.min_moves(7, 2) == 4
    assert bits_module.min_moves(8, 2) == 3
