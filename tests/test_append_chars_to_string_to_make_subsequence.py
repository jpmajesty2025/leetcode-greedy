from itertools import combinations

import pytest
from hypothesis import given, settings, strategies as st

import append_chars_to_string_to_make_subsequence as orig_module
import append_chars_to_string_to_make_subsequence_find as find_module
import append_chars_to_string_to_make_subsequence_iterator as iterator_module

IMPLS = [
    orig_module.append_characters,
    find_module.append_characters,
    iterator_module.append_characters,
]


def is_subsequence(t: str, s: str) -> bool:
    return any("".join(c) == t for c in combinations(s, len(t)))


def brute_force(s: str, t: str) -> int:
    """Smallest k such that some k-char suffix can be appended (the best choice is a suffix of t)."""
    for k in range(len(t) + 1):
        if is_subsequence(t, s + t[len(t) - k:]):
            return k
    raise AssertionError("unreachable: appending all of t always works")


@pytest.mark.parametrize("impl", IMPLS)
@pytest.mark.parametrize(
    "s, t, expected",
    [
        ("coaching", "coding", 4),        # LeetCode example 1
        ("abcde", "a", 0),                # LeetCode example 2
        ("z", "abcde", 5),                # LeetCode example 3
        ("", "", 0),
        ("abc", "", 0),                   # empty t is always a subsequence
        ("", "abc", 3),                   # empty s needs all of t
        ("abc", "abc", 0),                # identical
        ("abc", "abcd", 1),               # only the tail missing
        ("abcd", "abc", 0),               # t is a prefix of s
        ("abcd", "bd", 0),                # gaps allowed
        ("abc", "cba", 2),                # order matters
        ("aaa", "aaaa", 1),               # repeated letters
        ("aaaa", "aa", 0),
        ("xyz", "abc", 3),                # no overlap
        ("abxcd", "abcdef", 2),           # greedy earliest match
        ("b" * 1000 + "a", "ba", 0),      # match found late
    ],
)
def test_known_cases(impl, s, t, expected):
    assert impl(s, t) == expected


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_scale(impl):
    n = 100_000
    assert impl("a" * n, "a" * n) == 0
    assert impl("a" * n, "a" * (n - 1) + "b") == 1
    assert impl("a" * n, "b" * n) == n


@pytest.mark.parametrize("impl", IMPLS)
@settings(max_examples=400, deadline=None)
@given(
    s=st.text(alphabet="abc", max_size=8),
    t=st.text(alphabet="abc", max_size=6),
)
def test_matches_brute_force(impl, s, t):
    assert impl(s, t) == brute_force(s, t)


@settings(max_examples=500, deadline=None)
@given(
    s=st.text(alphabet="abcdefghijklmnopqrstuvwxyz", max_size=200),
    t=st.text(alphabet="abcdefghijklmnopqrstuvwxyz", max_size=200),
)
def test_implementations_agree_and_obey_bounds(s, t):
    results = {impl(s, t) for impl in IMPLS}
    assert len(results) == 1
    assert 0 <= results.pop() <= len(t)


@settings(max_examples=300, deadline=None)
@given(
    s=st.text(alphabet="abc", max_size=40),
    t=st.text(alphabet="abc", max_size=40),
)
def test_appending_the_answer_makes_t_a_subsequence(s, t):
    """Appending the last k characters of t must really work, and k - 1 must not."""
    k = orig_module.append_characters(s, t)
    assert _subseq(t, s + t[len(t) - k:])
    if k > 0:
        assert not _subseq(t, s + t[len(t) - k + 1:])


def _subseq(t: str, s: str) -> bool:
    it = iter(s)
    return all(c in it for c in t)


@settings(max_examples=300, deadline=None)
@given(
    s=st.text(alphabet="abc", max_size=40),
    t=st.text(alphabet="abc", max_size=40),
    extra=st.text(alphabet="abc", max_size=5),
)
def test_monotonic_properties(s, t, extra):
    base = orig_module.append_characters(s, t)
    assert orig_module.append_characters(s + extra, t) <= base        # more of s never hurts
    assert orig_module.append_characters(s, t + extra) >= base        # more of t never helps


@settings(max_examples=200, deadline=None)
@given(s=st.text(alphabet="abc", max_size=40))
def test_subsequence_of_s_needs_nothing(s):
    t = s[::2]  # every other character is certainly a subsequence
    assert all(impl(s, t) == 0 for impl in IMPLS)
