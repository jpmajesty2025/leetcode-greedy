import copy
from itertools import combinations

import pytest
from hypothesis import given, settings, strategies as st

import video_stiching as orig_module
import video_stiching_dp as dp_module
import video_stiching_reach_array as reach_module

IMPLS = [
    orig_module.video_stitching,
    reach_module.video_stitching,
    dp_module.video_stitching,
]


def covers(subset, time: int) -> bool:
    """True if the union of the clips covers every point of [0, time]."""
    reach = 0
    for start, end in sorted(subset):
        if start > reach:
            break
        reach = max(reach, end)
    return reach >= time


def brute_force(clips, time: int) -> int:
    if time == 0:
        return 0
    for size in range(1, len(clips) + 1):
        if any(covers(sub, time) for sub in combinations(clips, size)):
            return size
    return -1


clip_strategy = st.tuples(st.integers(0, 12), st.integers(0, 12)).filter(lambda c: c[0] < c[1]).map(list)


@pytest.mark.parametrize("impl", IMPLS)
@pytest.mark.parametrize(
    "clips, time, expected",
    [
        ([[0, 2], [4, 6], [8, 10], [1, 9], [1, 5], [5, 9]], 10, 3),   # LeetCode example 1
        ([[0, 1], [1, 2]], 5, -1),                                     # LeetCode example 2
        ([[0, 1], [6, 8], [0, 2], [5, 6], [0, 4], [0, 3], [6, 7], [1, 3], [4, 7], [1, 4], [2, 5], [2, 6],
          [3, 4], [4, 5], [5, 7], [6, 9]], 9, 3),                      # LeetCode example 3
        ([[0, 5]], 5, 1),                                              # one clip, exact fit
        ([[0, 9]], 5, 1),                                              # clip longer than the event
        ([], 5, -1),                                                   # no clips
        ([], 0, 0),                                                    # nothing to cover
        ([[3, 5]], 0, 0),                                              # nothing to cover, clip irrelevant
        ([[1, 5]], 5, -1),                                             # gap at the very start
        ([[0, 3], [4, 6]], 6, -1),                                     # gap in the middle
        ([[0, 3], [3, 6]], 6, 2),                                      # touching clips are enough
        ([[0, 3], [2, 6]], 6, 2),                                      # overlapping
        ([[0, 2], [2, 4], [4, 6], [0, 6]], 6, 1),                      # one clip beats a chain
        ([[0, 4], [2, 3], [3, 6]], 6, 2),                              # nested clip ignored
        ([[0, 4], [0, 4], [4, 8]], 8, 2),                              # duplicates
        ([[5, 10], [0, 5]], 10, 2),                                    # unsorted input
        ([[0, 1], [1, 2], [2, 3], [3, 4]], 4, 4),                      # forced chain
    ],
)
def test_known_cases(impl, clips, time, expected):
    assert impl(clips, time) == expected


@pytest.mark.parametrize("impl", IMPLS)
def test_input_is_not_modified(impl):
    """Regression: the original sorted the caller's list in place despite its docstring."""
    clips = [[5, 10], [0, 2], [1, 5]]
    snapshot = copy.deepcopy(clips)
    impl(clips, 10)
    assert clips == snapshot


@pytest.mark.parametrize("impl", IMPLS)
def test_negative_time_raises(impl):
    with pytest.raises(ValueError):
        impl([[0, 5]], -1)


@pytest.mark.parametrize("impl", IMPLS)
def test_clip_starting_before_zero_counts_from_zero(impl):
    assert impl([[-3, 4], [4, 8]], 8) == 2


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_scale(impl):
    time = 100
    chain = [[i, i + 1] for i in range(time)]
    assert impl(chain, time) == time                     # worst case: every clip needed
    assert impl(chain + [[0, time]], time) == 1          # one full clip wins


def test_greedy_versions_agree_with_many_clips():
    clips = [[i % 1000, i % 1000 + 1 + i % 7] for i in range(200_000)]
    assert orig_module.video_stitching(clips, 1000) == reach_module.video_stitching(clips, 1000)


@pytest.mark.parametrize("impl", IMPLS)
@settings(max_examples=300, deadline=None)
@given(clips=st.lists(clip_strategy, max_size=8), time=st.integers(min_value=0, max_value=12))
def test_matches_brute_force(impl, clips, time):
    assert impl(clips, time) == brute_force(clips, time)


@settings(max_examples=500, deadline=None)
@given(clips=st.lists(clip_strategy, max_size=30), time=st.integers(min_value=0, max_value=12))
def test_implementations_agree(clips, time):
    results = {impl(copy.deepcopy(clips), time) for impl in IMPLS}
    assert len(results) == 1
    result = results.pop()
    assert result == -1 or 0 <= result <= max(time, len(clips))


@settings(max_examples=300, deadline=None)
@given(
    clips=st.lists(clip_strategy, max_size=15),
    extra=clip_strategy,
    time=st.integers(min_value=1, max_value=12),
)
def test_adding_a_clip_never_hurts(clips, extra, time):
    before = reach_module.video_stitching(clips, time)
    after = reach_module.video_stitching(clips + [extra], time)
    if before != -1:
        assert after != -1 and after <= before
