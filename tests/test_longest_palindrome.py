from itertools import permutations
from string import ascii_letters

import pytest
from hypothesis import given, settings, strategies as st

import longest_palindrome as counter_module
import longest_palindrome_count as count_module
import longest_palindrome_toggle as toggle_module

IMPLS = [
    counter_module.longest_palindrome,
    toggle_module.longest_palindrome,
    count_module.longest_palindrome,
]


def is_palindrome(t: str) -> bool:
    return t == t[::-1]


def brute_force(s: str) -> int:
    """Longest palindromic rearrangement of any sub-multiset (tiny inputs only)."""
    best = 0
    n = len(s)
    for mask in range(1 << n):
        chosen = [s[i] for i in range(n) if mask >> i & 1]
        if len(chosen) <= best:
            continue
        if any(is_palindrome("".join(p)) for p in set(permutations(chosen))):
            best = len(chosen)
    return best


@pytest.mark.parametrize("impl", IMPLS)
@pytest.mark.parametrize(
    "s, expected",
    [
        ("abccccdd", 7),            # LeetCode example 1
        ("a", 1),                   # LeetCode example 2
        ("", 0),                    # empty string
        ("ab", 1),                  # all distinct: only a center
        ("aa", 2),                  # even pair
        ("aaa", 3),                 # odd count: use all, one in the center
        ("aabb", 4),                # all even
        ("abc", 1),
        ("aaabbb", 5),              # two odd counts: only one center
        ("Aa", 1),                  # case sensitive
        ("AaAa", 4),
        ("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", 1),  # all 52 letters once
        ("a" * 2000, 2000),         # LeetCode max length, one letter
        ("a" * 1999 + "b", 1999),   # two odd counts: all a's (one in the center), b unused
        ("ab" * 1000, 2000),        # many evens
        ("ab" * 1000 + "c", 2001),  # extra single becomes the center
        ("12321", 5),               # non-letters still work
    ],
)
def test_known_cases(impl, s, expected):
    assert impl(s) == expected


@pytest.mark.parametrize("impl", IMPLS)
@settings(max_examples=150, deadline=None)
@given(s=st.text(alphabet="abAB", max_size=9))
def test_matches_brute_force_on_small_inputs(impl, s):
    assert impl(s) == brute_force(s)


@settings(max_examples=500, deadline=None)
@given(s=st.text(alphabet=ascii_letters, max_size=300), seed=st.randoms(use_true_random=False))
def test_implementations_agree_and_obey_properties(s, seed):
    chars = list(s)
    seed.shuffle(chars)
    shuffled = "".join(chars)

    results = {impl(s) for impl in IMPLS} | {impl(shuffled) for impl in IMPLS}
    assert len(results) == 1  # all agree and anagrams give the same answer
    result = results.pop()

    assert 0 <= result <= len(s)
    if len(s):
        assert result >= 1
    odd_letters = sum(s.count(c) % 2 for c in set(s))
    assert result == len(s) - max(odd_letters - 1, 0)
    assert result % 2 == (1 if odd_letters else 0)  # length parity matches having a center


@pytest.mark.parametrize("impl", IMPLS)
@settings(max_examples=200, deadline=None)
@given(s=st.text(alphabet=ascii_letters, max_size=100), t=st.text(alphabet=ascii_letters, max_size=100))
def test_appending_never_shortens(impl, s, t):
    assert impl(s + t) >= impl(s)
