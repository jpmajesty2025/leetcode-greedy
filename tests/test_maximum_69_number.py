import pytest
from hypothesis import given, settings, strategies as st

import maximum_69_number as string_impl
import maximum_69_number_arithmetic as arithmetic_impl

IMPLS = [string_impl.maximum_69_number, arithmetic_impl.maximum_69_number]


def brute_force(num: int) -> int:
    """Try every single-digit flip, plus doing nothing."""
    digits = str(num)
    best = num
    for i, d in enumerate(digits):
        flipped = "9" if d == "6" else "6"
        best = max(best, int(digits[:i] + flipped + digits[i + 1:]))
    return best


digit_numbers = st.text(alphabet="69", min_size=1, max_size=18).map(int)


@pytest.mark.parametrize("impl", IMPLS)
@pytest.mark.parametrize(
    "num, expected",
    [
        (9669, 9969),    # LeetCode example 1
        (9996, 9999),    # LeetCode example 2
        (9999, 9999),    # already maximal
        (6, 9),          # single digit 6
        (9, 9),          # single digit 9
        (66, 96),        # only the leftmost 6 flips
        (666, 966),
        (6666, 9666),    # upper bound of LeetCode constraints
        (6999, 9999),    # leading 6
        (9969, 9999),
        (9699, 9999),
        (696969, 996969),
        (666666666666666666, 966666666666666666),  # 18 digits
    ],
)
def test_known_cases(impl, num, expected):
    assert impl(num) == expected


@pytest.mark.parametrize("impl", IMPLS)
@settings(max_examples=500, deadline=None)
@given(num=digit_numbers)
def test_matches_brute_force(impl, num):
    assert impl(num) == brute_force(num)


@pytest.mark.parametrize("impl", IMPLS)
@settings(max_examples=500, deadline=None)
@given(num=digit_numbers)
def test_result_properties(impl, num):
    result = impl(num)
    assert result >= num
    assert len(str(result)) == len(str(num))
    assert set(str(result)) <= {"6", "9"}
    differing = sum(a != b for a, b in zip(str(num), str(result)))
    assert differing <= 1
    # Only one flip per call: it removes at most one 6 (never adds one).
    assert str(result).count("6") >= str(num).count("6") - 1
    assert str(result).count("6") <= str(num).count("6")


@settings(max_examples=500, deadline=None)
@given(num=digit_numbers)
def test_implementations_agree(num):
    assert string_impl.maximum_69_number(num) == arithmetic_impl.maximum_69_number(num)


HUGE = 6 * (10**5000 - 1) // 9  # 5000 sixes, beyond Python's 4300-digit str() limit


def test_arithmetic_impl_handles_numbers_beyond_str_digit_limit():
    assert arithmetic_impl.maximum_69_number(HUGE) == HUGE + 3 * 10**4999


@pytest.mark.xfail(
    strict=True,
    raises=ValueError,
    reason="Known: str(num) raises past Python's default 4300-digit limit (outside LeetCode's range).",
)
def test_string_impl_handles_numbers_beyond_str_digit_limit():
    assert string_impl.maximum_69_number(HUGE) == HUGE + 3 * 10**4999
