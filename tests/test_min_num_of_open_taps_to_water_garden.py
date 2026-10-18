import copy
from itertools import combinations

import pytest
from hypothesis import given, settings, strategies as st

import min_num_of_open_taps_to_water_garden as orig_module
import min_num_of_open_taps_to_water_garden_dp as dp_module
import min_num_of_open_taps_to_water_garden_reach_array as reach_module

IMPLS = [
    orig_module.min_taps,
    reach_module.min_taps,
    dp_module.min_taps,
]


def covers(intervals, n: int) -> bool:
    """True if the union of the intervals covers every point of [0, n]."""
    reach = 0
    for left, right in sorted(intervals):
        if left > reach:
            break
        reach = max(reach, right)
    return reach >= n


def brute_force(n: int, ranges) -> int:
    intervals = [(i - r, i + r) for i, r in enumerate(ranges)]
    if n == 0:
        return 0
    for size in range(1, len(intervals) + 1):
        if any(covers(sub, n) for sub in combinations(intervals, size)):
            return size
    return -1


@pytest.mark.parametrize("impl", IMPLS)
@pytest.mark.parametrize(
    "n, ranges, expected",
    [
        (5, [3, 4, 1, 1, 0, 0], 1),                 # LeetCode example 1
        (3, [0, 0, 0, 0], -1),                      # LeetCode example 2
        (0, [0], 0),                                # empty garden
        (0, [5], 0),                                # empty garden, big tap
        (1, [0, 0], -1),
        (1, [1, 0], 1),                             # tap 0 reaches the end
        (1, [0, 1], 1),                             # tap 1 reaches the start
        (2, [0, 1, 0], 1),                          # middle tap covers everything
        (2, [1, 0, 1], 2),                          # touching intervals meet at point 1
        (4, [1, 0, 1, 0, 1], 3),                    # needs 0, 2 and 4; touching at 1 and 3
        (4, [2, 0, 0, 0, 2], 2),                    # two far taps meet in the middle
        (4, [1, 0, 0, 0, 1], -1),                   # gap around the middle
        (7, [1, 2, 1, 0, 2, 1, 0, 1], 3),
        (9, [0, 5, 0, 3, 3, 3, 1, 4, 0, 4], 2),
        (5, [5, 0, 0, 0, 0, 0], 1),                 # tap range larger than garden
        (5, [0, 0, 0, 0, 0, 5], 1),
    ],
)
def test_known_cases(impl, n, ranges, expected):
    assert impl(n, ranges) == expected


@pytest.mark.parametrize("impl", IMPLS)
def test_input_is_not_modified(impl):
    ranges = [3, 4, 1, 1, 0, 0]
    snapshot = copy.deepcopy(ranges)
    impl(5, ranges)
    assert ranges == snapshot


@pytest.mark.parametrize("impl", IMPLS)
@pytest.mark.parametrize(
    "n, ranges",
    [
        (-1, [0]),                  # negative n
        (3, [1, 1, 1]),             # too short
        (3, [1, 1, 1, 1, 1]),       # too long
        (2, [1, -1, 1]),            # negative range
        (1, [-5, 0]),
    ],
)
def test_invalid_input_raises(impl, n, ranges):
    with pytest.raises(ValueError):
        impl(n, ranges)


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_scale(impl):
    n = 10_000
    assert impl(n, [1] * (n + 1)) == orig_module.min_taps(n, [1] * (n + 1))
    # one huge tap in the middle waters everything
    ranges = [0] * (n + 1)
    ranges[n // 2] = n
    assert impl(n, ranges) == 1
    # range-1 taps at even positions only: taps 0, 2, 4, ..., n are all needed (they just touch)
    assert impl(n, [1 if i % 2 == 0 else 0 for i in range(n + 1)]) == n // 2 + 1


def test_dp_agrees_with_greedy_on_a_moderate_input():
    n = 300
    ranges = [(i * 7) % 11 for i in range(n + 1)]
    assert dp_module.min_taps(n, ranges) == reach_module.min_taps(n, ranges)


@pytest.mark.parametrize("impl", IMPLS)
@settings(max_examples=300, deadline=None)
@given(data=st.data(), n=st.integers(min_value=0, max_value=8))
def test_matches_brute_force(impl, data, n):
    ranges = data.draw(st.lists(st.integers(0, 4), min_size=n + 1, max_size=n + 1))
    assert impl(n, ranges) == brute_force(n, ranges)


@settings(max_examples=500, deadline=None)
@given(data=st.data(), n=st.integers(min_value=0, max_value=60))
def test_implementations_agree_and_obey_bounds(data, n):
    ranges = data.draw(st.lists(st.integers(0, 12), min_size=n + 1, max_size=n + 1))
    results = {impl(n, list(ranges)) for impl in IMPLS}
    assert len(results) == 1
    result = results.pop()
    assert result == -1 or 0 <= result <= n + 1
    if n > 0 and result != -1:
        assert result >= 1


@settings(max_examples=300, deadline=None)
@given(data=st.data(), n=st.integers(min_value=1, max_value=30), i=st.integers(min_value=0, max_value=30), extra=st.integers(1, 5))
def test_bigger_range_never_hurts(data, n, i, extra):
    ranges = data.draw(st.lists(st.integers(0, 8), min_size=n + 1, max_size=n + 1))
    i = i % (n + 1)
    bigger = list(ranges)
    bigger[i] += extra
    before = reach_module.min_taps(n, ranges)
    after = reach_module.min_taps(n, bigger)
    if before != -1:
        assert after != -1 and after <= before
