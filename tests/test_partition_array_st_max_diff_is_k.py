import pytest
from hypothesis import given, settings, strategies as st

import partition_array_st_max_diff_is_k as sort_impl
import partition_array_st_max_diff_is_k_presence as presence_impl

IMPLS = [sort_impl.partition_array, presence_impl.partition_array]


def oracle(nums: list[int], k: int) -> int:
    """Independent check: greedily peel groups from the smallest value using a multiset."""
    remaining = sorted(nums)
    groups = 0
    while remaining:
        floor = remaining[0]
        remaining = [x for x in remaining if x > floor + k]
        groups += 1
    return groups


def exhaustive(nums: list[int], k: int) -> int:
    """True optimum by trying every set partition (tiny inputs only)."""
    best = len(nums)

    def place(i, groups):
        nonlocal best
        if len(groups) >= best:
            return
        if i == len(nums):
            best = len(groups)
            return
        for g in groups:
            if max(max(g), nums[i]) - min(min(g), nums[i]) <= k:
                g.append(nums[i])
                place(i + 1, groups)
                g.pop()
        groups.append([nums[i]])
        place(i + 1, groups)
        groups.pop()

    place(0, [])
    return best


@pytest.mark.parametrize("impl", IMPLS)
@pytest.mark.parametrize(
    "nums, k, expected",
    [
        ([3, 6, 1, 2, 5], 2, 2),   # LeetCode example 1
        ([1, 2, 3], 1, 2),         # LeetCode example 2
        ([2, 2, 4, 5], 0, 3),      # LeetCode example 3
        ([7], 0, 1),               # singleton
        ([5, 5, 5, 5], 0, 1),      # all duplicates, k = 0
        ([1, 3], 2, 1),            # difference exactly k stays together
        ([1, 4], 2, 2),            # difference k + 1 splits
        ([0, 100000], 100000, 1),  # max range, max k
        ([0, 100000], 99999, 2),
        ([1, 2, 3, 4, 5, 6], 1, 3),  # chain: groups {1,2} {3,4} {5,6}
        ([10, 1, 9, 2, 8, 3], 2, 2),  # unsorted input
        ([-5, -3, 0, 4], 3, 3),    # negative values
    ],
)
def test_known_cases(impl, nums, k, expected):
    assert impl(list(nums), k) == expected


@pytest.mark.parametrize("impl", IMPLS)
def test_large_input(impl):
    nums = list(range(100000))
    assert impl(list(nums), 0) == 100000
    assert impl(list(nums), 99999) == 1


@pytest.mark.parametrize("impl", IMPLS)
def test_input_order_does_not_matter(impl):
    assert impl([6, 5, 3, 2, 1], 2) == impl([1, 2, 3, 5, 6], 2) == 2


@pytest.mark.xfail(
    strict=True,
    reason="Known: nums.sort() mutates the caller's list. Remove after switching to sorted().",
)
def test_sort_impl_does_not_mutate_input():
    nums = [3, 6, 1, 2, 5]
    sort_impl.partition_array(nums, 2)
    assert nums == [3, 6, 1, 2, 5]


def test_presence_impl_does_not_mutate_input():
    nums = [3, 6, 1, 2, 5]
    presence_impl.partition_array(nums, 2)
    assert nums == [3, 6, 1, 2, 5]


def test_presence_impl_empty_returns_zero():
    assert presence_impl.partition_array([], 3) == 0


@pytest.mark.xfail(
    strict=True,
    raises=IndexError,
    reason="Known: empty input raises IndexError at nums[0] (outside LeetCode's n >= 1).",
)
def test_sort_impl_empty_returns_zero():
    assert sort_impl.partition_array([], 3) == 0


@pytest.mark.parametrize("impl", IMPLS)
@settings(max_examples=300, deadline=None)
@given(
    nums=st.lists(st.integers(min_value=0, max_value=12), min_size=1, max_size=8),
    k=st.integers(min_value=0, max_value=12),
)
def test_matches_exhaustive_partition_search(impl, nums, k):
    assert impl(list(nums), k) == exhaustive(nums, k)


@pytest.mark.parametrize("impl", IMPLS)
@settings(max_examples=300, deadline=None)
@given(
    nums=st.lists(st.integers(min_value=0, max_value=10**5), min_size=1, max_size=200),
    k=st.integers(min_value=0, max_value=10**5),
)
def test_matches_oracle_and_bounds(impl, nums, k):
    result = impl(list(nums), k)
    assert result == oracle(nums, k)
    assert 1 <= result <= len(set(nums))
    if max(nums) - min(nums) <= k:
        assert result == 1


@settings(max_examples=300, deadline=None)
@given(
    nums=st.lists(st.integers(min_value=-1000, max_value=1000), min_size=1, max_size=100),
    k=st.integers(min_value=0, max_value=2000),
)
def test_implementations_agree(nums, k):
    assert sort_impl.partition_array(list(nums), k) == presence_impl.partition_array(list(nums), k)


@settings(max_examples=200, deadline=None)
@given(
    nums=st.lists(st.integers(min_value=0, max_value=1000), min_size=1, max_size=100),
    k=st.integers(min_value=0, max_value=1000),
)
def test_larger_k_never_needs_more_groups(nums, k):
    assert presence_impl.partition_array(list(nums), k + 1) <= presence_impl.partition_array(list(nums), k)
