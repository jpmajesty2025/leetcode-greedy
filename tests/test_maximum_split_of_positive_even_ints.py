from functools import lru_cache
from math import isqrt

import pytest
from hypothesis import given, settings, strategies as st

import maximum_split_of_positive_even_ints as orig_module
import maximum_split_of_positive_even_ints_closed_form as closed_module
import maximum_split_of_positive_even_ints_lookahead as lookahead_module

IMPLS = [
    orig_module.maximum_even_split,
    closed_module.maximum_even_split,
    lookahead_module.maximum_even_split,
]


def assert_valid_split(total: int, parts: list[int]) -> None:
    assert all(p > 0 and p % 2 == 0 for p in parts)
    assert len(set(parts)) == len(parts)
    assert sum(parts) == total


@lru_cache(maxsize=None)
def max_parts_brute(total: int, smallest: int = 2) -> int:
    """Most distinct even parts >= smallest summing to total, by exhaustive search; -1 if impossible."""
    if total == 0:
        return 0
    best = -1
    for part in range(smallest, total + 1, 2):
        rest = max_parts_brute(total - part, part + 2)
        if rest >= 0:
            best = max(best, rest + 1)
    return best


@pytest.mark.parametrize("impl", IMPLS)
@pytest.mark.parametrize(
    "final_sum, expected_count",
    [
        (12, 3),                 # LeetCode example 1: 2 + 4 + 6
        (7, 0),                  # LeetCode example 2: odd
        (28, 4),                 # LeetCode example 3: e.g. 2 + 4 + 6 + 16
        (2, 1),                  # smallest valid
        (4, 1),                  # 4 only: 2 + 2 is not unique
        (6, 2),                  # 2 + 4
        (8, 2),                  # 2 + 6
        (10, 2),                 # 2 + 8: 2 + 4 + 4 repeats a 4
        (30, 5),                 # 2 + 4 + 6 + 8 + 10 exactly, no leftover
    ],
)
def test_known_counts(impl, final_sum, expected_count):
    parts = impl(final_sum)
    assert len(parts) == expected_count
    if expected_count:
        assert_valid_split(final_sum, parts)


@pytest.mark.parametrize("impl", IMPLS)
@pytest.mark.parametrize("final_sum", [12, 28, 2, 4, 6, 30, 42])
def test_exact_outputs_are_increasing_with_last_adjusted(impl, final_sum):
    parts = impl(final_sum)
    assert parts == sorted(parts)
    assert_valid_split(final_sum, parts)


@pytest.mark.parametrize("impl", IMPLS)
def test_specific_outputs(impl):
    assert impl(12) == [2, 4, 6]
    assert impl(10) == [2, 8]
    assert impl(8) == [2, 6]
    assert impl(28) == [2, 4, 6, 16]     # leftover 8 lands on the last element
    assert impl(30) == [2, 4, 6, 8, 10]  # exact triangular sum: no leftover


@pytest.mark.parametrize("impl", IMPLS)
@pytest.mark.parametrize("bad", [7, 1, 3, -2, -7, 0, -100, 99999])
def test_no_valid_split_returns_empty(impl, bad):
    assert impl(bad) == []


@pytest.mark.parametrize("impl", IMPLS)
def test_does_not_modify_a_returned_list_across_calls(impl):
    first = impl(12)
    first.append(999)
    assert impl(12) == [2, 4, 6]  # no shared state between calls


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_scale(impl):
    total = 10**10
    parts = impl(total)
    assert_valid_split(total, parts)
    k = len(parts)
    assert k * (k + 1) <= total < (k + 1) * (k + 2)  # k parts fit, k + 1 would not


@pytest.mark.parametrize("impl", IMPLS)
@settings(max_examples=60, deadline=None)
@given(half=st.integers(min_value=1, max_value=60))
def test_matches_brute_force_count(impl, half):
    total = 2 * half
    parts = impl(total)
    assert_valid_split(total, parts)
    assert len(parts) == max_parts_brute(total)


@settings(max_examples=500, deadline=None)
@given(final_sum=st.integers(min_value=-10, max_value=10**6))
def test_implementations_agree_and_obey_bounds(final_sum):
    results = [impl(final_sum) for impl in IMPLS]
    assert results[0] == results[1] == results[2]
    parts = results[0]
    if final_sum <= 0 or final_sum % 2:
        assert parts == []
    else:
        assert_valid_split(final_sum, parts)
        k = len(parts)
        assert k == (isqrt(8 * (final_sum // 2) + 1) - 1) // 2  # independent closed-form count
        assert k * (k + 1) <= final_sum


@settings(max_examples=300, deadline=None)
@given(half=st.integers(min_value=1, max_value=10**5))
def test_count_is_monotonic_and_grows_by_at_most_one(half):
    a = len(orig_module.maximum_even_split(2 * half))
    b = len(orig_module.maximum_even_split(2 * half + 2))
    assert 0 <= b - a <= 1
