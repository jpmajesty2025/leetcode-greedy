from itertools import permutations

import pytest
from hypothesis import given, settings, strategies as st

import destroying_asteroids as sort_impl
import destroying_asteroids_heap as heap_impl


def brute_force(mass: int, asteroids: list[int]) -> bool:
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
        (10, [3, 9, 19, 5, 21], True),
        (5, [4, 9, 23, 4], False),
        (1, [], True),
        (1, [1], True),
        (1, [2], False),
        (1, [1, 2, 4, 8, 16], True),
        (1, [1, 2, 4, 9], False),
        (3, [100, 1, 1, 1], False),
        (10**5, [10**5] * 10**5, True),
    ],
)
def test_known_cases(mass, asteroids, expected):
    assert heap_impl.asteroids_destroyed(mass, list(asteroids)) is expected


def test_does_not_mutate_input():
    asteroids = [3, 9, 19, 5, 21]
    heap_impl.asteroids_destroyed(10, asteroids)
    assert asteroids == [3, 9, 19, 5, 21]


@settings(max_examples=300, deadline=None)
@given(
    mass=st.integers(min_value=1, max_value=30),
    asteroids=st.lists(st.integers(min_value=1, max_value=60), max_size=7),
)
def test_matches_brute_force(mass, asteroids):
    assert heap_impl.asteroids_destroyed(mass, asteroids) == brute_force(mass, asteroids)


@settings(max_examples=300, deadline=None)
@given(
    mass=st.integers(min_value=1, max_value=10**5),
    asteroids=st.lists(st.integers(min_value=1, max_value=10**5), max_size=60),
)
def test_agrees_with_sort_implementation(mass, asteroids):
    assert heap_impl.asteroids_destroyed(mass, asteroids) == sort_impl.asteroids_destroyed(
        mass, list(asteroids)
    )
