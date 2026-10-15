from itertools import combinations

import pytest
from hypothesis import given, settings, strategies as st

import reduce_array_size_by_half as orig_module
import reduce_array_size_by_half_buckets as bucket_module


def original(arr):
    """The original takes a stray `self`; pass None so we can test the algorithm itself."""
    return orig_module.min_set_size(None, list(arr))


def buckets(arr):
    return bucket_module.min_set_size(list(arr))


IMPLS = [original, buckets]


def exhaustive(arr: list[int]) -> int:
    """True optimum: smallest set of distinct values removing at least half (tiny inputs only)."""
    distinct = sorted(set(arr))
    need = (len(arr) + 1) // 2
    for size in range(len(distinct) + 1):
        for chosen in combinations(distinct, size):
            if sum(1 for x in arr if x in chosen) >= need:
                return size
    return len(distinct)


@pytest.mark.parametrize("impl", IMPLS)
@pytest.mark.parametrize(
    "arr, expected",
    [
        ([3, 3, 3, 3, 5, 5, 5, 2, 2, 7], 2),   # LeetCode example 1
        ([7, 7, 7, 7, 7, 7], 1),               # LeetCode example 2
        ([1, 2], 1),                           # two distinct values
        ([1, 1], 1),
        ([1, 2, 3, 4], 2),                     # all distinct, even length
        ([1, 1, 2, 2], 1),                     # exact half removed by one value
        ([1, 1, 2, 3, 4, 5], 2),               # needs 3 of 6: both 1s + one single
        ([1, 1, 1, 2, 2, 3], 1),               # one value covers exactly half
        ([1, 1, 2, 2, 3, 3, 4, 4], 2),         # all frequencies tied
        ([5] * 100000, 1),                     # large, one value
        (list(range(100000)), 50000),          # large, all distinct
        ([i // 2 for i in range(100000)], 25000),  # large, all frequency 2
        ([-1, -1, -1, 2, 3, 4], 1),            # negative values
    ],
)
def test_known_cases(impl, arr, expected):
    assert impl(arr) == expected


@pytest.mark.parametrize("impl", IMPLS)
def test_empty_returns_zero(impl):
    assert impl([]) == 0


@pytest.mark.parametrize("impl", IMPLS)
def test_does_not_mutate_input(impl):
    arr = [3, 3, 3, 3, 5, 5, 5, 2, 2, 7]
    impl(arr)
    assert arr == [3, 3, 3, 3, 5, 5, 5, 2, 2, 7]


@pytest.mark.parametrize("impl", IMPLS)
def test_input_order_does_not_matter(impl):
    assert impl([7, 2, 3, 5, 3, 2, 3, 5, 3, 5]) == impl([3, 3, 3, 3, 5, 5, 5, 2, 2, 7]) == 2


@pytest.mark.xfail(
    strict=True,
    raises=TypeError,
    reason="Known: min_set_size has a stray `self` parameter (a LeetCode class-method paste), "
    "so calling min_set_size(arr) raises TypeError.",
)
def test_original_is_callable_with_just_the_array():
    assert orig_module.min_set_size([1, 1, 2, 2]) == 1


@pytest.mark.xfail(
    strict=True,
    reason="Known: len(arr) // 2 floors for odd lengths; 'at least half' needs ceil. "
    "LeetCode guarantees even length, so this is outside the judge's range.",
)
def test_original_handles_odd_length():
    assert original([1, 2, 3]) == 2  # 3 elements: removing 1 element is less than half


def test_buckets_handles_odd_length():
    assert buckets([1, 2, 3]) == 2
    assert buckets([1, 1, 2]) == 1
    assert buckets([1, 2, 3, 4, 5]) == 3


@pytest.mark.parametrize("impl", IMPLS)
@settings(max_examples=300, deadline=None)
@given(arr=st.lists(st.integers(min_value=0, max_value=6), max_size=7).filter(lambda a: len(a) % 2 == 0))
def test_matches_exhaustive_for_even_lengths(impl, arr):
    assert impl(arr) == exhaustive(arr)


@settings(max_examples=300, deadline=None)
@given(arr=st.lists(st.integers(min_value=0, max_value=6), max_size=9))
def test_buckets_matches_exhaustive_for_any_length(arr):
    assert buckets(arr) == exhaustive(arr)


@settings(max_examples=300, deadline=None)
@given(
    arr=st.lists(st.integers(min_value=-50, max_value=50), max_size=200).filter(lambda a: len(a) % 2 == 0),
    seed=st.randoms(use_true_random=False),
)
def test_implementations_agree_and_obey_bounds(arr, seed):
    shuffled = list(arr)
    seed.shuffle(shuffled)
    a = original(arr)
    assert a == buckets(arr) == buckets(shuffled)
    assert 0 <= a <= len(set(arr))
    if arr:
        assert a >= 1
