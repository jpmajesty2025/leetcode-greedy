from functools import lru_cache
from itertools import product
from string import ascii_lowercase

import pytest
from hypothesis import given, settings, strategies as st

import smallest_string_with_a_given_numeric_value as orig_module
import smallest_string_with_a_given_numeric_value_closed_form as closed_module
import smallest_string_with_a_given_numeric_value_forward as forward_module

IMPLS = [
    orig_module.get_smallest_string,
    closed_module.get_smallest_string,
    forward_module.get_smallest_string,
]


def value(s: str) -> int:
    return sum(ord(c) - 96 for c in s)


@lru_cache(maxsize=None)
def _brute_table(n: int) -> dict:
    """Map each reachable numeric value to the smallest string of length n (exhaustive, n <= 3)."""
    table = {}
    for letters in product(ascii_lowercase, repeat=n):  # product yields lexicographic order
        s = "".join(letters)
        table.setdefault(value(s), s)
    return table


def dp_oracle(n: int, k: int) -> str:
    """Independent oracle: pick the smallest letter at each position that keeps a completion feasible,
    where feasibility is decided by a memoised DP rather than the 26*n bound."""

    @lru_cache(maxsize=None)
    def feasible(length: int, total: int) -> bool:
        if length == 0:
            return total == 0
        return any(feasible(length - 1, total - v) for v in range(1, 27) if total - v >= 0)

    out, remaining = [], k
    for length in range(n, 0, -1):
        v = next(v for v in range(1, 27) if remaining - v >= 0 and feasible(length - 1, remaining - v))
        out.append(chr(96 + v))
        remaining -= v
    return "".join(out)


@pytest.mark.parametrize("impl", IMPLS)
@pytest.mark.parametrize(
    "n, k, expected",
    [
        (3, 27, "aay"),                 # LeetCode example 1
        (5, 73, "aaszz"),               # LeetCode example 2
        (1, 1, "a"),                    # minimum
        (1, 26, "z"),
        (1, 13, "m"),
        (2, 2, "aa"),                   # all 'a'
        (2, 52, "zz"),                  # all 'z'
        (3, 78, "zzz"),
        (2, 26, "ay"),                  # 24 extra fits in one char
        (2, 27, "az"),                  # 25 extra: exactly one z
        (2, 28, "bz"),                  # 26 extra: spills into the previous char
        (3, 3, "aaa"),
        (4, 30, "aabz"),                # 26 extra: one z plus a 'b' beside it
    ],
)
def test_known_cases(impl, n, k, expected):
    assert impl(n, k) == expected


@pytest.mark.parametrize("impl", IMPLS)
def test_empty_string(impl):
    assert impl(0, 0) == ""


@pytest.mark.parametrize("impl", IMPLS)
@pytest.mark.parametrize(
    "n, k",
    [
        (1, 0),        # k below n
        (3, 2),        # k below n
        (1, 27),       # one over the max
        (3, 79),       # one over the max
        (2, 100),      # far over the max
        (0, 1),        # no characters can have a positive value
        (-1, 0),       # negative length
    ],
)
def test_impossible_inputs_raise(impl, n, k):
    with pytest.raises(ValueError):
        impl(n, k)


@pytest.mark.parametrize("impl", IMPLS)
def test_large_extremes(impl):
    n = 100_000
    assert impl(n, n) == "a" * n
    assert impl(n, 26 * n) == "z" * n
    s = impl(n, 13 * n)
    assert len(s) == n and value(s) == 13 * n


@pytest.mark.parametrize("impl", IMPLS)
@pytest.mark.parametrize("n", [1, 2, 3])
def test_exhaustive_small_alphabet_matches_brute_force(impl, n):
    """Every valid (n, k) for n <= 3 against an exhaustive search over all 26**n strings."""
    for k, expected in _brute_table(n).items():
        assert impl(n, k) == expected, (n, k)
    assert set(_brute_table(n)) == set(range(n, 26 * n + 1))  # valid range is exactly n..26n


@pytest.mark.parametrize("impl", IMPLS)
@settings(max_examples=300, deadline=None)
@given(data=st.data(), n=st.integers(min_value=1, max_value=12))
def test_matches_dp_oracle(impl, data, n):
    k = data.draw(st.integers(min_value=n, max_value=26 * n))
    assert impl(n, k) == dp_oracle(n, k)


@settings(max_examples=500, deadline=None)
@given(data=st.data(), n=st.integers(min_value=1, max_value=1000))
def test_implementations_agree_and_satisfy_invariants(data, n):
    k = data.draw(st.integers(min_value=n, max_value=26 * n))
    results = {impl(n, k) for impl in IMPLS}
    assert len(results) == 1
    s = results.pop()
    assert len(s) == n and value(s) == k
    # shape: non-decreasing letters, with at most one letter strictly between 'a' and 'z'
    assert list(s) == sorted(s)
    assert sum(1 for c in s if c not in "az") <= 1


@settings(max_examples=300, deadline=None)
@given(data=st.data(), n=st.integers(min_value=1, max_value=200))
def test_monotonic_in_k(data, n):
    """A larger target value never yields a lexicographically smaller string."""
    k = data.draw(st.integers(min_value=n, max_value=26 * n - 1))
    assert closed_module.get_smallest_string(n, k) < closed_module.get_smallest_string(n, k + 1)
