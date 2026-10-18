import pytest
from hypothesis import given, settings, strategies as st

import min_addition_to_make_integer_beautiful as orig_module
import min_addition_to_make_integer_beautiful_prefix as prefix_module
import min_addition_to_make_integer_beautiful_quotient as quotient_module

IMPLS = [
    orig_module.make_integer_beautiful,
    prefix_module.make_integer_beautiful,
    quotient_module.make_integer_beautiful,
]


def digit_sum(num: int) -> int:
    return sum(map(int, str(num)))


def brute_force(n: int, target: int) -> int:
    x = 0
    while digit_sum(n + x) > target:
        x += 1
    return x


@pytest.mark.parametrize("impl", IMPLS)
@pytest.mark.parametrize(
    "n, target, expected",
    [
        (16, 6, 4),               # LeetCode example 1: 16 -> 20
        (467, 6, 33),             # LeetCode example 2: 467 -> 500
        (1, 1, 0),                # LeetCode example 3: already beautiful
        (12, 8, 0),
        (19, 1, 81),              # 19 -> 100
        (999, 1, 1),              # 999 -> 1000
        (99, 1, 1),
        (95, 1, 5),               # carries into the tens: 95 -> 100
        (195, 2, 5),              # 195 -> 200
        (1999, 2, 1),             # 1999 -> 2000
        (1900, 2, 100),           # 1900 -> 2000
        (100, 1, 0),              # a power of ten is always beautiful
        (500, 5, 0),              # digit sum equals target exactly
        (506, 5, 494),            # 510 and 600 both have digit sum 6, so round all the way to 1000
    ],
)
def test_known_cases(impl, n, target, expected):
    assert impl(n, target) == expected


@pytest.mark.parametrize("impl", IMPLS)
@pytest.mark.parametrize("n, target", [(0, 5), (-3, 5), (10, 0), (10, -1)])
def test_invalid_input_raises(impl, n, target):
    with pytest.raises(ValueError):
        impl(n, target)


def test_original_regression_cases():
    """The original jumped to the next power of ten instead of the next multiple of 10, 100, ..."""
    assert orig_module.make_integer_beautiful(16, 6) == 4      # was 84
    assert orig_module.make_integer_beautiful(467, 6) == 33    # was 533


@pytest.mark.parametrize("impl", IMPLS)
def test_exhaustive_small_range_against_brute_force(impl):
    for n in range(1, 1500):
        for target in (1, 2, 3, 5, 8, 12, 20):
            assert impl(n, target) == brute_force(n, target), (n, target)


@pytest.mark.parametrize("impl", IMPLS)
def test_large_values(impl):
    n = 10**18 - 1                     # eighteen 9s
    assert impl(n, 1) == 1
    n = 123456789012345678
    x = impl(n, 5)
    assert digit_sum(n + x) <= 5
    assert x < 10 ** len(str(n))       # never needs more than rounding up to the next power of ten


@settings(max_examples=500, deadline=None)
@given(n=st.integers(min_value=1, max_value=20_000), target=st.integers(min_value=1, max_value=36))
def test_matches_brute_force_on_random_inputs(n, target):
    expected = brute_force(n, target)
    assert {impl(n, target) for impl in IMPLS} == {expected}


@settings(max_examples=1000, deadline=None)
@given(n=st.integers(min_value=1, max_value=10**18), target=st.integers(min_value=1, max_value=162))
def test_implementations_agree_and_result_is_valid(n, target):
    results = {impl(n, target) for impl in IMPLS}
    assert len(results) == 1
    x = results.pop()
    assert x >= 0
    assert digit_sum(n + x) <= target
    if x > 0:
        assert digit_sum(n) > target                    # we only add when needed
        assert (n + x) % 10 == 0                        # any addition ends on a multiple of 10
        assert x < 10 ** len(str(n))                    # bounded by rounding up to the next power of ten


@settings(max_examples=300, deadline=None)
@given(n=st.integers(min_value=1, max_value=10**9), target=st.integers(min_value=1, max_value=80))
def test_larger_target_never_needs_more(n, target):
    assert prefix_module.make_integer_beautiful(n, target + 1) <= prefix_module.make_integer_beautiful(n, target)
