from itertools import permutations

import pytest
from hypothesis import given, settings, strategies as st

import assign_cookies as orig_module
import assign_cookies_heaps as heaps_module
import assign_cookies_sorted as sorted_module


def original(g, s):
    """The original sorts its arguments in place, so hand it copies in comparisons."""
    return orig_module.find_content_children(list(g), list(s))


def refactored(g, s):
    return sorted_module.find_content_children(list(g), list(s))


def heaps(g, s):
    return heaps_module.find_content_children(list(g), list(s))


IMPLS = [original, refactored, heaps]


def brute_force(g: list[int], s: list[int]) -> int:
    """Best matching by trying every assignment of cookies to children (tiny inputs only)."""
    best = 0
    for order in permutations(range(len(s)), min(len(g), len(s))):
        content = sum(1 for child, cookie in enumerate(order) if s[cookie] >= g[child])
        best = max(best, content)
    # also cover assigning to different child subsets when there are more children than cookies
    if len(g) > len(s):
        for kids in permutations(range(len(g)), len(s)):
            content = sum(1 for cookie, child in enumerate(kids) if s[cookie] >= g[child])
            best = max(best, content)
    return best


@pytest.mark.parametrize("impl", IMPLS)
@pytest.mark.parametrize(
    "g, s, expected",
    [
        ([1, 2, 3], [1, 1], 1),               # LeetCode example 1
        ([1, 2], [1, 2, 3], 2),               # LeetCode example 2
        ([], [1, 2, 3], 0),                   # no children
        ([1, 2, 3], [], 0),                   # no cookies
        ([], [], 0),
        ([1], [1], 1),                        # exact fit
        ([2], [1], 0),                        # too small
        ([1, 1, 1], [1, 1, 1], 3),            # everyone matches
        ([5, 5, 5], [4, 4, 4], 0),            # nobody matches
        ([1, 2, 3], [3, 3, 3], 3),            # big cookies satisfy all
        ([3, 2, 1], [1, 2, 3], 3),            # unsorted inputs
        ([10, 9, 8, 7], [5, 6, 7, 8], 2),     # only the 7 and 8 cookies fit
        ([1, 2, 3], [100], 1),                # one huge cookie feeds only one child
        ([100], [1, 2, 3], 0),                # many small cookies cannot combine
        ([1, 1, 2, 2], [2, 2], 2),            # cookies go to the least greedy
        ([2**31 - 1], [2**31 - 1], 1),        # 32-bit max values
        (list(range(1, 30001)), list(range(1, 30001)), 30000),  # LeetCode-scale
    ],
)
def test_known_cases(impl, g, s, expected):
    assert impl(g, s) == expected


@pytest.mark.parametrize("impl", [refactored, heaps])
def test_does_not_mutate_inputs(impl):
    g, s = [3, 1, 2], [2, 3, 1]
    impl_module = sorted_module if impl is refactored else heaps_module
    impl_module.find_content_children(g, s)
    assert g == [3, 1, 2] and s == [2, 3, 1]


@pytest.mark.xfail(
    strict=True,
    reason="Known: g.sort() and s.sort() reorder the caller's lists. Remove after switching to sorted().",
)
def test_original_does_not_mutate_inputs():
    g, s = [3, 1, 2], [2, 3, 1]
    orig_module.find_content_children(g, s)
    assert g == [3, 1, 2] and s == [2, 3, 1]


@pytest.mark.parametrize("impl", IMPLS)
@settings(max_examples=300, deadline=None)
@given(
    g=st.lists(st.integers(min_value=1, max_value=6), max_size=5),
    s=st.lists(st.integers(min_value=1, max_value=6), max_size=5),
)
def test_matches_brute_force(impl, g, s):
    assert impl(g, s) == brute_force(g, s)


@settings(max_examples=400, deadline=None)
@given(
    g=st.lists(st.integers(min_value=1, max_value=2**31 - 1), max_size=60),
    s=st.lists(st.integers(min_value=1, max_value=2**31 - 1), max_size=60),
    seed=st.randoms(use_true_random=False),
)
def test_implementations_agree_and_obey_bounds(g, s, seed):
    g2, s2 = list(g), list(s)
    seed.shuffle(g2)
    seed.shuffle(s2)
    results = {impl(g, s) for impl in IMPLS} | {impl(g2, s2) for impl in IMPLS}
    assert len(results) == 1  # all agree and order does not matter
    assert 0 <= results.pop() <= min(len(g), len(s))


@settings(max_examples=300, deadline=None)
@given(
    g=st.lists(st.integers(min_value=1, max_value=50), max_size=30),
    s=st.lists(st.integers(min_value=1, max_value=50), max_size=30),
    extra=st.integers(min_value=1, max_value=50),
)
def test_monotonic_in_resources(g, s, extra):
    base = refactored(g, s)
    assert refactored(g, s + [extra]) >= base      # an extra cookie never hurts
    assert refactored(g + [extra], s) >= base      # an extra child never hurts
    assert refactored(g + [extra], s) <= base + 1  # ...and adds at most one content child
