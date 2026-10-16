import pytest
from hypothesis import given, settings, strategies as st

import maximum_ice_cream_bars as orig_module
import maximum_ice_cream_bars_counting as counting_module
import maximum_ice_cream_bars_sorted as sorted_module


def original(costs, coins):
    """The original takes a stray `self`; pass None so we can test the algorithm itself."""
    return orig_module.max_ice_cream(None, list(costs), coins)


def counting(costs, coins):
    return counting_module.max_ice_cream(list(costs), coins)


def sorted_impl(costs, coins):
    return sorted_module.max_ice_cream(list(costs), coins)


IMPLS = [original, counting, sorted_impl]


def brute_force(costs: list[int], coins: int) -> int:
    """Independent oracle: cheapest-first using a running sum over sorted prices."""
    total = 0
    count = 0
    for cost in sorted(costs):
        if total + cost > coins:
            break
        total += cost
        count += 1
    return count


def exhaustive(costs: list[int], coins: int) -> int:
    """True optimum over every subset (tiny inputs only)."""
    best = 0
    n = len(costs)
    for mask in range(1 << n):
        picked = [costs[i] for i in range(n) if mask >> i & 1]
        if sum(picked) <= coins:
            best = max(best, len(picked))
    return best


@pytest.mark.parametrize("impl", IMPLS)
@pytest.mark.parametrize(
    "costs, coins, expected",
    [
        ([1, 3, 2, 4, 1], 7, 4),            # LeetCode example 1
        ([10, 6, 8, 7, 7, 8], 5, 0),        # LeetCode example 2
        ([1, 6, 3, 1, 2, 5], 20, 6),        # LeetCode example 3
        ([], 10, 0),                        # no bars
        ([5], 5, 1),                        # exact change
        ([5], 4, 0),                        # one coin short
        ([1, 1, 1], 0, 0),                  # no coins
        ([2, 2, 2, 2], 7, 3),               # duplicates, coins left over
        ([100000], 10**8, 1),               # max price
        ([1] * 100000, 10**8, 100000),      # buys everything
        ([100000] * 1000, 10**8, 1000),     # exactly affordable
        ([100000] * 1001, 10**8, 1000),     # one too many
        ([4, 1, 3, 2], 6, 3),               # unsorted input: 1 + 2 + 3
        ([1, 100000], 100000, 1),           # expensive bar skipped, remainder unused
    ],
)
def test_known_cases(impl, costs, coins, expected):
    assert impl(costs, coins) == expected


@pytest.mark.parametrize("impl", IMPLS)
def test_does_not_mutate_input(impl):
    costs = [4, 1, 3, 2, 1]
    impl(costs, 6)
    assert costs == [4, 1, 3, 2, 1]


@pytest.mark.xfail(
    strict=True,
    raises=TypeError,
    reason="Known: max_ice_cream has a stray `self` parameter (a LeetCode class-method paste), "
    "so calling max_ice_cream(costs, coins) raises TypeError.",
)
def test_original_is_callable_with_just_costs_and_coins():
    assert orig_module.max_ice_cream([1, 3, 2, 4, 1], 7) == 4


@pytest.mark.parametrize("impl", [original, counting])
def test_zero_cost_bars_are_free(impl):
    assert impl([0, 0, 3], 0) == 2
    assert impl([0, 5], 4) == 1


def test_sorted_impl_handles_zero_cost_and_huge_prices():
    assert sorted_impl([0, 0, 3], 0) == 2
    assert sorted_impl([10**12, 10**12 + 1, 5], 10**12) == 1  # sparse range: no bucket array needed


@pytest.mark.parametrize("impl", IMPLS)
@settings(max_examples=300, deadline=None)
@given(
    costs=st.lists(st.integers(min_value=1, max_value=12), max_size=9),
    coins=st.integers(min_value=0, max_value=60),
)
def test_matches_exhaustive_subset_search(impl, costs, coins):
    assert impl(costs, coins) == exhaustive(costs, coins)


@settings(max_examples=300, deadline=None)
@given(
    costs=st.lists(st.integers(min_value=1, max_value=1000), max_size=200),
    coins=st.integers(min_value=0, max_value=10**5),
    seed=st.randoms(use_true_random=False),
)
def test_all_implementations_agree_and_are_order_invariant(costs, coins, seed):
    shuffled = list(costs)
    seed.shuffle(shuffled)
    expected = brute_force(costs, coins)
    for impl in IMPLS:
        assert impl(costs, coins) == expected
        assert impl(shuffled, coins) == expected
    assert 0 <= expected <= len(costs)


@settings(max_examples=200, deadline=None)
@given(
    costs=st.lists(st.integers(min_value=0, max_value=50), max_size=40),
    coins=st.integers(min_value=0, max_value=500),
)
def test_more_coins_never_buys_fewer_bars(costs, coins):
    assert counting(costs, coins + 1) >= counting(costs, coins)
    assert counting(costs, coins) == sorted_impl(costs, coins)
