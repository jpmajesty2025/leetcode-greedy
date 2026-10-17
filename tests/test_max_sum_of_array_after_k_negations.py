from itertools import product

import pytest
from hypothesis import given, settings, strategies as st

import max_sum_of_array_after_k_negations_counting as counting_module
import max_sum_of_array_after_k_negations_heap as heap_module
import max_sum_of_array_after_k_negations_sorted as sorted_module


def sorted_impl(nums, k):
    return sorted_module.largest_sum_after_k_negations(list(nums), k)


def heap(nums, k):
    return heap_module.largest_sum_after_k_negations(list(nums), k)


def counting(nums, k):
    return counting_module.largest_sum_after_k_negations(list(nums), k)


IMPLS = [sorted_impl, heap, counting]


def brute_force(nums: list[int], k: int) -> int:
    """Try every sequence of k index choices (tiny inputs only)."""
    best = None
    for picks in product(range(len(nums)), repeat=k):
        arr = list(nums)
        for i in picks:
            arr[i] = -arr[i]
        total = sum(arr)
        best = total if best is None else max(best, total)
    return best


@pytest.mark.parametrize("impl", IMPLS)
@pytest.mark.parametrize(
    "nums, k, expected",
    [
        ([4, 2, 3], 1, 5),                    # LeetCode example 1
        ([3, -1, 0, 2], 3, 6),                # LeetCode example 2
        ([2, -3, -1, 5, -4], 2, 13),          # LeetCode example 3
        ([5], 1, -5),                         # forced to negate the only element
        ([5], 2, 5),                          # even flips cancel
        ([-5], 1, 5),
        ([-5], 2, -5),                        # second flip undoes the first
        ([-5], 3, 5),
        ([0], 100, 0),                        # zero absorbs any flips
        ([1, 2, 3], 3, 4),                    # all positive, odd k: flip the smallest
        ([1, 2, 3], 4, 6),                    # all positive, even k: nothing lost
        ([-1, -2, -3], 2, 4),                 # flip the two most negative: 3 + 2 - 1
        ([-1, -2, -3], 3, 6),                 # flip all three
        ([-1, -2, -3], 4, 4),                 # extra flip lands on the smallest (1)
        ([-4, -2, 3], 5, 5),                  # 4 + 2 + 3, then one leftover flip on the 2: 4 - 2 + 3
        ([-1, 0, 1], 1, 2),
        ([-3, -3, -3], 2, 3),                 # duplicates of the most negative value
        ([-100, 100], 10000, 0),              # LeetCode max k
        ([-100] * 10000, 10000, 1000000),     # LeetCode max size: flips everything
        ([100] * 10000, 9999, 100 * 10000 - 2 * 100),  # odd k on all-positive input
    ],
)
def test_known_cases(impl, nums, k, expected):
    assert impl(nums, k) == expected


@pytest.mark.parametrize("module", [sorted_module, heap_module, counting_module])
def test_does_not_mutate_input(module):
    arr = [2, -3, -1, 5, -4]
    module.largest_sum_after_k_negations(arr, 2)
    assert arr == [2, -3, -1, 5, -4]


@pytest.mark.parametrize("impl", IMPLS)
@settings(max_examples=300, deadline=None)
@given(
    nums=st.lists(st.integers(min_value=-6, max_value=6), min_size=1, max_size=5),
    k=st.integers(min_value=1, max_value=5),
)
def test_matches_brute_force(impl, nums, k):
    assert impl(nums, k) == brute_force(nums, k)


@settings(max_examples=500, deadline=None)
@given(
    nums=st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=200),
    k=st.integers(min_value=1, max_value=500),
    seed=st.randoms(use_true_random=False),
)
def test_implementations_agree_and_obey_bounds(nums, k, seed):
    shuffled = list(nums)
    seed.shuffle(shuffled)
    results = {impl(nums, k) for impl in IMPLS} | {impl(shuffled, k) for impl in IMPLS}
    assert len(results) == 1  # all agree and order does not matter
    result = results.pop()
    assert result <= sum(abs(x) for x in nums)
    assert result >= -sum(abs(x) for x in nums)
    assert result % 2 == sum(nums) % 2  # each flip changes the sum by an even amount


@settings(max_examples=300, deadline=None)
@given(
    nums=st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=60),
    k=st.integers(min_value=1, max_value=200),
)
def test_k_and_k_plus_two_agree_once_negatives_are_exhausted(nums, k):
    negatives = sum(1 for x in nums if x < 0)
    if k >= negatives:
        assert sorted_impl(nums, k) == sorted_impl(nums, k + 2)
