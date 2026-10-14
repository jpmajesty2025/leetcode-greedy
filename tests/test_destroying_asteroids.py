from itertools import permutations

import pytest
from hypothesis import given, settings, strategies as st

from destroying_asteroids import asteroids_destroyed


def brute_force(mass: int, asteroids: list[int]) -> bool:
    """Independent oracle: try every collision order."""
    if not asteroids:
        return True
    for order in permutations(asteroids):
        m = mass
        for a in order:
            if m < a:
                break
            m += a
        else:
            return True
    return False


@pytest.mark.parametrize(
    "mass, asteroids, expected",
    [
        (10, [3, 9, 19, 5, 21], True),   # LeetCode example 1
        (5, [4, 9, 23, 4], False),       # LeetCode example 2
        (1, [], True),                   # no asteroids
        (1, [1], True),                  # equal mass is destroyed (>=)
        (1, [2], False),                 # one too heavy
        (1, [1, 2, 4, 8, 16], True),     # doubling chain, exact boundaries
        (1, [1, 2, 4, 9], False),        # chain breaks at the last step
        (5, [5, 5, 5, 5], True),         # duplicates
        (3, [100, 1, 1, 1], False),      # one unreachable giant
        (1, [1] * 1000, True),           # many small ones
        (10**5, [10**5] * 10**5, True),  # upper-bound-sized input
    ],
)
def test_known_cases(mass, asteroids, expected):
    assert asteroids_destroyed(mass, list(asteroids)) is expected


def test_input_order_does_not_matter():
    assert asteroids_destroyed(10, [21, 19, 9, 5, 3]) is True
    assert asteroids_destroyed(10, [3, 5, 9, 19, 21]) is True


@pytest.mark.xfail(
    strict=True,
    reason="Known: asteroids.sort() mutates the caller's list. "
    "Remove this marker after switching to sorted().",
)
def test_does_not_mutate_input():
    asteroids = [3, 9, 19, 5, 21]
    asteroids_destroyed(10, asteroids)
    assert asteroids == [3, 9, 19, 5, 21]


@settings(max_examples=300, deadline=None)
@given(
    mass=st.integers(min_value=1, max_value=30),
    asteroids=st.lists(st.integers(min_value=1, max_value=60), max_size=7),
)
def test_matches_brute_force(mass, asteroids):
    assert asteroids_destroyed(mass, list(asteroids)) == brute_force(mass, asteroids)


@settings(max_examples=200, deadline=None)
@given(
    mass=st.integers(min_value=1, max_value=10**5),
    asteroids=st.lists(st.integers(min_value=1, max_value=10**5), max_size=50),
    seed=st.randoms(use_true_random=False),
)
def test_permutation_invariant(mass, asteroids, seed):
    shuffled = list(asteroids)
    seed.shuffle(shuffled)
    assert asteroids_destroyed(mass, list(asteroids)) == asteroids_destroyed(mass, shuffled)


@settings(max_examples=200, deadline=None)
@given(
    mass=st.integers(min_value=1, max_value=100),
    asteroids=st.lists(st.integers(min_value=1, max_value=100), max_size=30),
)
def test_more_mass_never_hurts(mass, asteroids):
    if asteroids_destroyed(mass, list(asteroids)):
        assert asteroids_destroyed(mass + 1, list(asteroids))
