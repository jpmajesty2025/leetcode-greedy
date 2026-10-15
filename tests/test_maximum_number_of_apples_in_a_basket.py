from itertools import combinations

import pytest
from hypothesis import given, settings, strategies as st

import maximum_number_of_apples_in_a_basket as sort_impl
import maximum_number_of_apples_in_a_basket_buckets as bucket_impl

IMPLS = [sort_impl.max_number_of_apples, bucket_impl.max_number_of_apples]


def exhaustive(weight: list[int], capacity: int = 5000) -> int:
    """True optimum: largest subset whose total weight fits (tiny inputs only)."""
    for size in range(len(weight), 0, -1):
        for subset in combinations(weight, size):
            if sum(subset) <= capacity:
                return size
    return 0


@pytest.mark.parametrize("impl", IMPLS)
@pytest.mark.parametrize(
    "weight, expected",
    [
        ([100, 200, 150, 1000], 4),                # LeetCode example 1
        ([900, 950, 800, 1000, 700, 800], 5),      # LeetCode example 2
        ([], 0),                                   # no apples
        ([5000], 1),                               # exactly fills the basket
        ([5001], 0),                               # one apple too heavy
        ([1], 1),                                  # lightest apple
        ([2500, 2500], 2),                         # two apples exactly fill it
        ([2500, 2500, 1], 2),                      # one extra no longer fits
        ([1000] * 5, 5),                           # boundary: total 5000
        ([1000] * 6, 5),                           # boundary: total 6000
        ([4999, 1, 1], 2),                         # prefers the two lightest
        ([5000, 1, 1, 1], 3),                      # heavy one skipped
        ([1] * 1000, 1000),                        # LeetCode max, all fit
        ([1000] * 1000, 5),                        # LeetCode max, heavy
        ([1] * 6000, 5000),                        # more apples than capacity
    ],
)
def test_known_cases(impl, weight, expected):
    assert impl(list(weight)) == expected


@pytest.mark.parametrize("impl", IMPLS)
def test_input_order_does_not_matter(impl):
    assert impl([1000, 100, 150, 200]) == impl([100, 200, 150, 1000]) == 4


@pytest.mark.xfail(
    strict=True,
    reason="Known: weight.sort() reorders the caller's list. Remove after switching to sorted().",
)
def test_sort_impl_does_not_mutate_input():
    weight = [900, 950, 800, 1000, 700, 800]
    sort_impl.max_number_of_apples(weight)
    assert weight == [900, 950, 800, 1000, 700, 800]


def test_bucket_impl_does_not_mutate_input():
    weight = [900, 950, 800, 1000, 700, 800]
    bucket_impl.max_number_of_apples(weight)
    assert weight == [900, 950, 800, 1000, 700, 800]


@pytest.mark.parametrize(
    "weight, capacity, expected",
    [
        ([3, 1, 2], 0, 0),
        ([3, 1, 2], 3, 2),
        ([3, 1, 2], 6, 3),
        ([3, 1, 2], 5, 2),
        ([], 10, 0),
    ],
)
def test_bucket_impl_custom_capacity(weight, capacity, expected):
    assert bucket_impl.max_number_of_apples(weight, capacity) == expected


@pytest.mark.parametrize("impl", IMPLS)
@settings(max_examples=300, deadline=None)
@given(weight=st.lists(st.integers(min_value=1, max_value=2000), max_size=10))
def test_matches_exhaustive_subset_search(impl, weight):
    assert impl(list(weight)) == exhaustive(weight)


@settings(max_examples=300, deadline=None)
@given(
    weight=st.lists(st.integers(min_value=1, max_value=12), max_size=10),
    capacity=st.integers(min_value=0, max_value=40),
)
def test_bucket_impl_matches_exhaustive_for_any_capacity(weight, capacity):
    assert bucket_impl.max_number_of_apples(list(weight), capacity) == exhaustive(weight, capacity)


@settings(max_examples=300, deadline=None)
@given(
    weight=st.lists(st.integers(min_value=1, max_value=1000), max_size=300),
    seed=st.randoms(use_true_random=False),
)
def test_implementations_agree_and_are_order_invariant(weight, seed):
    shuffled = list(weight)
    seed.shuffle(shuffled)
    a = sort_impl.max_number_of_apples(list(weight))
    assert a == bucket_impl.max_number_of_apples(list(weight)) == bucket_impl.max_number_of_apples(shuffled)
    assert 0 <= a <= len(weight)
    assert sum(sorted(weight)[:a]) <= 5000  # the chosen apples really fit
    if a < len(weight):
        assert sum(sorted(weight)[: a + 1]) > 5000  # and one more would not


@settings(max_examples=200, deadline=None)
@given(
    weight=st.lists(st.integers(min_value=1, max_value=1000), max_size=100),
    capacity=st.integers(min_value=0, max_value=10**4),
)
def test_bigger_basket_never_holds_fewer(weight, capacity):
    assert bucket_impl.max_number_of_apples(weight, capacity + 1) >= bucket_impl.max_number_of_apples(
        weight, capacity
    )
