from itertools import combinations_with_replacement

import pytest
from hypothesis import given, settings, strategies as st

import maximum_units_on_a_truck as sort_impl
import maximum_units_on_a_truck_buckets as bucket_impl

IMPLS = [sort_impl.maximum_units, bucket_impl.maximum_units]


def brute_force(box_types: list[list[int]], truck_size: int) -> int:
    """Expand every box individually and take the best truck_size of them."""
    boxes = [units for count, units in box_types for _ in range(count)]
    return sum(sorted(boxes, reverse=True)[:truck_size])


def exhaustive(box_types: list[list[int]], truck_size: int) -> int:
    """True optimum over every multiset of boxes of the right size (tiny inputs only)."""
    boxes = [units for count, units in box_types for _ in range(count)]
    size = min(truck_size, len(boxes))
    best = 0
    for chosen in set(combinations_with_replacement(range(len(boxes)), size)):
        if len(set(chosen)) == len(chosen):  # each physical box used at most once
            best = max(best, sum(boxes[i] for i in chosen))
    return best


@pytest.mark.parametrize("impl", IMPLS)
@pytest.mark.parametrize(
    "box_types, truck_size, expected",
    [
        ([[1, 3], [2, 2], [3, 1]], 4, 8),          # LeetCode example 1
        ([[5, 10], [2, 5], [4, 7], [3, 9]], 10, 91),  # LeetCode example 2
        ([], 5, 0),                                # no box types
        ([[3, 4]], 0, 0),                          # empty truck
        ([[1, 1]], 1, 1),                          # single box
        ([[5, 7]], 3, 21),                         # truck smaller than supply
        ([[2, 7]], 10, 14),                        # truck larger than supply
        ([[1, 5], [1, 5], [1, 5]], 2, 10),         # duplicate unit values
        ([[3, 1], [2, 2], [1, 3]], 6, 10),         # ascending input order
        ([[1000, 1000]] * 1000, 10**6, 10**9),     # max-ish values, truck exactly full
        ([[1000, 1000]] * 1000, 10**7, 10**9),     # truck larger than all boxes
    ],
)
def test_known_cases(impl, box_types, truck_size, expected):
    assert impl([list(b) for b in box_types], truck_size) == expected


@pytest.mark.xfail(
    strict=True,
    reason="Known: boxTypes.sort() reorders the caller's list. Remove after switching to sorted().",
)
def test_sort_impl_does_not_mutate_input():
    box_types = [[1, 3], [2, 2], [3, 1], [4, 9]]
    snapshot = [list(b) for b in box_types]
    sort_impl.maximum_units(box_types, 4)
    assert box_types == snapshot


def test_bucket_impl_does_not_mutate_input():
    box_types = [[1, 3], [2, 2], [3, 1], [4, 9]]
    snapshot = [list(b) for b in box_types]
    bucket_impl.maximum_units(box_types, 4)
    assert box_types == snapshot


box_type_lists = st.lists(
    st.tuples(st.integers(min_value=1, max_value=6), st.integers(min_value=1, max_value=12)).map(list),
    max_size=6,
)


@pytest.mark.parametrize("impl", IMPLS)
@settings(max_examples=300, deadline=None)
@given(box_types=box_type_lists, truck_size=st.integers(min_value=0, max_value=40))
def test_matches_brute_force(impl, box_types, truck_size):
    assert impl([list(b) for b in box_types], truck_size) == brute_force(box_types, truck_size)


@pytest.mark.parametrize("impl", IMPLS)
@settings(max_examples=200, deadline=None)
@given(
    box_types=st.lists(
        st.tuples(st.integers(min_value=1, max_value=3), st.integers(min_value=1, max_value=9)).map(list),
        max_size=4,
    ),
    truck_size=st.integers(min_value=0, max_value=8),
)
def test_matches_exhaustive_selection(impl, box_types, truck_size):
    assert impl([list(b) for b in box_types], truck_size) == exhaustive(box_types, truck_size)


@settings(max_examples=300, deadline=None)
@given(
    box_types=st.lists(
        st.tuples(st.integers(min_value=1, max_value=1000), st.integers(min_value=1, max_value=1000)).map(list),
        max_size=50,
    ),
    truck_size=st.integers(min_value=0, max_value=10**5),
    seed=st.randoms(use_true_random=False),
)
def test_implementations_agree_and_are_order_invariant(box_types, truck_size, seed):
    shuffled = [list(b) for b in box_types]
    seed.shuffle(shuffled)
    a = sort_impl.maximum_units([list(b) for b in box_types], truck_size)
    b = bucket_impl.maximum_units([list(x) for x in box_types], truck_size)
    c = bucket_impl.maximum_units(shuffled, truck_size)
    assert a == b == c
    total_boxes = sum(n for n, _ in box_types)
    assert a <= min(truck_size, total_boxes) * max((u for _, u in box_types), default=0)


@settings(max_examples=200, deadline=None)
@given(box_types=box_type_lists, truck_size=st.integers(min_value=0, max_value=40))
def test_bigger_truck_never_hurts(box_types, truck_size):
    assert bucket_impl.maximum_units(box_types, truck_size + 1) >= bucket_impl.maximum_units(
        box_types, truck_size
    )
