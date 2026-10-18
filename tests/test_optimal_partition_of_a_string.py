from itertools import product

import pytest
from hypothesis import given, settings, strategies as st

import optimal_partition_of_a_string as orig_module
import optimal_partition_of_a_string_bitmask as bitmask_module
import optimal_partition_of_a_string_last_seen as last_seen_module

IMPLS = [
    orig_module.partition_string,
    bitmask_module.partition_string,
    last_seen_module.partition_string,
]


def brute_force(s: str) -> int:
    """Try every way of cutting s (2**(n-1) cut sets) and keep the fewest all-unique pieces."""
    n = len(s)
    if n == 0:
        return 1
    best = n
    for cuts in product([False, True], repeat=n - 1):
        pieces, start = [], 0
        for i, cut in enumerate(cuts, start=1):
            if cut:
                pieces.append(s[start:i])
                start = i
        pieces.append(s[start:])
        if all(len(set(p)) == len(p) for p in pieces):
            best = min(best, len(pieces))
    return best


@pytest.mark.parametrize("impl", IMPLS)
@pytest.mark.parametrize(
    "s, expected",
    [
        ("abacaba", 4),                  # LeetCode example 1
        ("ssssss", 6),                   # LeetCode example 2
        ("a", 1),                        # singleton
        ("", 1),                         # documented: one or more substrings
        ("ab", 1),
        ("aa", 2),
        ("abcdefghijklmnopqrstuvwxyz", 1),        # full alphabet, no repeat
        ("abcdefghijklmnopqrstuvwxyza", 2),       # repeat only at the very end
        ("abcabc", 2),
        ("abcab", 2),
        ("abab", 2),                     # greedy cut is not at the first repeat's partner
        ("aabb", 3),
        ("abba", 2),                     # second 'a' is only a repeat if the 'b's did not reset
        ("abcdabcd", 2),
    ],
)
def test_known_cases(impl, s, expected):
    assert impl(s) == expected


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_scale(impl):
    n = 100_000
    assert impl("a" * n) == n                                  # worst case: every char alone
    assert impl(("abcdefghijklmnopqrstuvwxyz" * 4000)[:n]) == -(-n // 26)  # ceil(n / 26) pieces


@pytest.mark.parametrize("impl", IMPLS)
def test_callable_with_a_single_string_argument(impl):
    """Regression: the original once had a stray `self` parameter and raised TypeError here."""
    assert impl("abc") == 1


@pytest.mark.parametrize("impl", [bitmask_module.partition_string])
@pytest.mark.parametrize("bad", ["A", "a1", "a b", "é"])
def test_bitmask_rejects_non_lowercase(impl, bad):
    with pytest.raises(ValueError):
        impl(bad)


def test_last_seen_handles_any_characters():
    assert last_seen_module.partition_string("aAaA") == 2
    assert last_seen_module.partition_string("1212") == 2


@pytest.mark.parametrize("impl", IMPLS)
@settings(max_examples=400, deadline=None)
@given(s=st.text(alphabet="abc", max_size=12))
def test_matches_brute_force(impl, s):
    assert impl(s) == brute_force(s)


@settings(max_examples=500, deadline=None)
@given(s=st.text(alphabet="abcdefghijklmnopqrstuvwxyz", max_size=300))
def test_implementations_agree_and_obey_bounds(s):
    results = {impl(s) for impl in IMPLS}
    assert len(results) == 1
    r = results.pop()
    assert 1 <= r <= max(1, len(s))
    assert r >= -(-len(s) // 26)  # a piece holds at most 26 distinct letters


@settings(max_examples=300, deadline=None)
@given(s=st.text(alphabet="abcdefghijklmnopqrstuvwxyz", max_size=100))
def test_greedy_pieces_are_valid_and_cover_s(s):
    """Reconstruct the greedy pieces and check they concatenate to s and each is all-unique."""
    pieces, current = [], ""
    for ch in s:
        if ch in current:
            pieces.append(current)
            current = ""
        current += ch
    pieces.append(current)
    assert "".join(pieces) == s
    assert all(len(set(p)) == len(p) for p in pieces)
    assert len(pieces) == orig_module.partition_string(s)


@settings(max_examples=300, deadline=None)
@given(
    s=st.text(alphabet="abc", max_size=40),
    extra=st.text(alphabet="abc", max_size=5),
)
def test_monotonic_under_extension_and_prefix(s, extra):
    base = orig_module.partition_string(s)
    assert orig_module.partition_string(s + extra) >= base          # longer never needs fewer
    assert orig_module.partition_string(s + extra) <= base + len(extra)
    assert orig_module.partition_string(s[: len(s) // 2]) <= base   # prefix never needs more
