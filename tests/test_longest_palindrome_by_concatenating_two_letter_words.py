from itertools import permutations

import pytest
from hypothesis import given, settings, strategies as st

import longest_palindrome_by_concatenating_two_letter_words as orig_module
import longest_palindrome_by_concatenating_two_letter_words_fixed as fixed_module
import longest_palindrome_by_concatenating_two_letter_words_streaming as streaming_module

original = orig_module.longest_palindrome
fixed = fixed_module.longest_palindrome
streaming = streaming_module.longest_palindrome

CORRECT_IMPLS = [fixed, streaming]
ALL_IMPLS = [original, fixed, streaming]


def is_palindrome(t: str) -> bool:
    return t == t[::-1]


def brute_force(words: list[str]) -> int:
    """Try every ordered selection of words (tiny inputs only)."""
    best = 0
    n = len(words)
    for size in range(1, n + 1):
        for order in set(permutations(words, size)):
            joined = "".join(order)
            if is_palindrome(joined):
                best = max(best, len(joined))
    return best


# Cases the original handles correctly (it works when the first-seen word has the larger count).
@pytest.mark.parametrize("impl", ALL_IMPLS)
@pytest.mark.parametrize(
    "words, expected",
    [
        (["lc", "cl", "gg"], 6),                          # LeetCode example 1
        (["ab", "ty", "yt", "lc", "cl", "ab"], 8),        # LeetCode example 2
        (["cc", "ll", "xx"], 2),                          # LeetCode example 3
        ([], 0),                                          # no words
        (["ab"], 0),                                      # no mirror
        (["aa"], 2),                                      # lone palindrome becomes the center
        (["aa", "aa"], 4),                                # pair of identical palindromes
        (["aa", "aa", "aa"], 6),                          # pair plus center
        (["aa", "bb"], 2),                                # only one center allowed
        (["aa", "aa", "bb"], 6),                          # pair of aa plus bb center
        (["ab", "ba"], 4),
        (["ab", "ba", "ab", "ba"], 8),
        (["ab", "ab", "ba"], 4),                          # larger count seen first
        (["ab", "cd", "dc", "ba", "aa"], 10),             # mix of pairs and a center
        (["ab", "ac", "ad"], 0),                          # shared letters but no mirrors
    ],
)
def test_known_cases(impl, words, expected):
    assert impl(list(words)) == expected


# Inputs where the original double counts: the first-seen word has the smaller count.
BUG_CASES = [
    (["ba", "ab", "ab", "ab"], 4),
    (["ab", "ba", "ba", "ba"], 4),
    (["ba", "ab", "ab"], 4),
    (["ab", "ba", "ba", "aa"], 6),
]


@pytest.mark.parametrize("impl", CORRECT_IMPLS)
@pytest.mark.parametrize("words, expected", BUG_CASES)
def test_unequal_mirror_counts_in_either_order(impl, words, expected):
    assert impl(list(words)) == expected


@pytest.mark.xfail(
    strict=True,
    reason="Known bug: when the first-seen of a mirror pair has the smaller count, the original "
    "decrements only the partner, so the leftover partners are counted again.",
)
@pytest.mark.parametrize("words, expected", BUG_CASES)
def test_original_unequal_mirror_counts_in_either_order(words, expected):
    assert original(list(words)) == expected


@pytest.mark.parametrize("impl", ALL_IMPLS)
def test_does_not_mutate_input(impl):
    words = ["lc", "cl", "gg", "ab", "ba"]
    snapshot = list(words)
    impl(words)
    assert words == snapshot


@pytest.mark.parametrize("impl", CORRECT_IMPLS)
def test_large_inputs(impl):
    assert impl(["ab", "ba"] * 50000) == 4 * 50000
    assert impl(["aa"] * 100000) == 4 * 50000
    assert impl(["aa"] * 99999) == 4 * 49999 + 2
    assert impl(["ab"] * 100000) == 0
    assert impl(["ab"] * 70000 + ["ba"] * 30000) == 4 * 30000


@pytest.mark.parametrize("impl", CORRECT_IMPLS)
@settings(max_examples=200, deadline=None)
@given(words=st.lists(st.sampled_from(["ab", "ba", "aa", "bb", "ac"]), max_size=7))
def test_matches_brute_force_on_small_inputs(impl, words):
    assert impl(list(words)) == brute_force(words)


words_strategy = st.lists(
    st.text(alphabet="abcd", min_size=2, max_size=2), max_size=60
)


@settings(max_examples=400, deadline=None)
@given(words=words_strategy, seed=st.randoms(use_true_random=False))
def test_fixed_and_streaming_agree_and_are_order_invariant(words, seed):
    shuffled = list(words)
    seed.shuffle(shuffled)
    expected = fixed(list(words))
    assert streaming(list(words)) == expected
    assert fixed(shuffled) == expected
    assert streaming(shuffled) == expected
    assert expected % 2 == 0 and 0 <= expected <= 2 * len(words)


@settings(max_examples=300, deadline=None)
@given(words=words_strategy)
def test_matches_independent_formula(words):
    """Closed-form oracle computed from counts alone."""
    from collections import Counter

    c = Counter(words)
    total = 0
    center = False
    for w, n in c.items():
        r = w[::-1]
        if w == r:
            total += (n // 2) * 4
            center = center or n % 2 == 1
        elif w < r:
            total += min(n, c.get(r, 0)) * 4
    total += 2 if center else 0
    assert fixed(list(words)) == total


@settings(max_examples=200, deadline=None)
@given(words=words_strategy, extra=st.text(alphabet="abcd", min_size=2, max_size=2))
def test_adding_a_word_never_shortens(words, extra):
    assert fixed(words + [extra]) >= fixed(words)
