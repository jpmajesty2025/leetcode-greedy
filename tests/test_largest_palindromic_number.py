from itertools import permutations

import pytest
from hypothesis import given, settings, strategies as st
from collections import Counter

import largest_palindromic_number as orig_module
import largest_palindromic_number_counting as counting_module
import largest_palindromic_number_two_pointer as two_pointer_module

IMPLS = [
    orig_module.largest_palindromic,
    counting_module.largest_palindromic,
    two_pointer_module.largest_palindromic,
]


def is_valid_integer_string(s: str) -> bool:
    return s == "0" or (s != "" and s[0] != "0")


def brute_force(num: str) -> str:
    """Try every non-empty ordered selection of digits (tiny inputs only); keep the numerically largest
    palindrome without leading zeros."""
    best = ""
    for length in range(1, len(num) + 1):
        for chosen in set(permutations(num, length)):
            s = "".join(chosen)
            if s == s[::-1] and is_valid_integer_string(s):
                if (len(s), s) > (len(best), best):
                    best = s
    return best


@pytest.mark.parametrize("impl", IMPLS)
@pytest.mark.parametrize(
    "num, expected",
    [
        ("444947137", "7449447"),        # LeetCode example 1
        ("00009", "9"),                  # LeetCode example 2
        ("0000", "0"),                   # only zeros collapses to "0" (LeetCode answer)
        ("0", "0"),
        ("00", "0"),
        ("5", "5"),
        ("55", "55"),
        ("12", "2"),                     # no pair: largest single digit
        ("0001", "1"),                   # zeros would only pad with leading zeros
        ("0011", "1001"),                # zeros inside are fine
        ("00011", "10001"),
        ("000", "0"),
        ("9900", "9009"),
        ("99900", "90909"),              # odd 9s: one is the centre, zero pair goes inside
        ("123321", "321123"),
        ("1223334", "32423"),            # pairs 3 and 2; largest leftover (4) is the centre
        ("121", "121"),
        ("1233", "323"),                 # longer beats bigger digits: 323 > 33
        ("123", "3"),
    ],
)
def test_known_cases(impl, num, expected):
    assert impl(num) == expected


@pytest.mark.parametrize("impl", IMPLS)
@pytest.mark.parametrize("bad", ["", "12a", "-1", "1 2", "١٢"])
def test_invalid_input_raises(impl, bad):
    with pytest.raises(ValueError):
        impl(bad)


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_scale(impl):
    n = 100_000
    assert impl("9" * n) == "9" * n
    assert impl("0" * n) == "0"
    assert impl("9" * (n - 1) + "8") == "9" * (n - 1)  # odd 9 is the centre; the lone 8 is unused
    result = impl("0123456789" * (n // 10))             # every digit pairs evenly
    assert len(result) == n and result[0] == "9" and result[-1] == "9"


@pytest.mark.parametrize("impl", IMPLS)
@settings(max_examples=400, deadline=None)
@given(num=st.text(alphabet="0123456789", min_size=1, max_size=6))
def test_matches_brute_force(impl, num):
    assert impl(num) == brute_force(num)


@settings(max_examples=500, deadline=None)
@given(num=st.text(alphabet="0123456789", min_size=1, max_size=200))
def test_implementations_agree_and_result_is_valid(num):
    results = {impl(num) for impl in IMPLS}
    assert len(results) == 1
    r = results.pop()
    assert r == r[::-1]                              # palindrome
    assert is_valid_integer_string(r)                # no leading zeros
    available, used = Counter(num), Counter(r)
    assert all(used[d] <= available[d] for d in used)  # only digits we actually have


@settings(max_examples=300, deadline=None)
@given(num=st.text(alphabet="0123456789", min_size=1, max_size=100), seed=st.randoms(use_true_random=False))
def test_order_of_digits_is_irrelevant(num, seed):
    shuffled = list(num)
    seed.shuffle(shuffled)
    assert orig_module.largest_palindromic("".join(shuffled)) == orig_module.largest_palindromic(num)


@settings(max_examples=300, deadline=None)
@given(num=st.text(alphabet="0123456789", min_size=1, max_size=60), extra=st.sampled_from("0123456789"))
def test_adding_a_digit_never_shrinks_the_answer(num, extra):
    before = orig_module.largest_palindromic(num)
    after = orig_module.largest_palindromic(num + extra)
    assert (len(after), after) >= (len(before), before)
