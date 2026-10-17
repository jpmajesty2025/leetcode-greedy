"""
Append Characters to String to Make Subsequence: Shared-Iterator Idiom.

1. Wrap s in a single iterator. `char in iterator` advances it up to and including the first match.
2. Walk t in order; each character found consumes the iterator past its match.
3. After the first miss the iterator is exhausted, so every later character misses too. That means
   counting hits counts exactly the matched prefix of t.

Short and idiomatic, but it relies on the side effect of `in` on an iterator, which is easy to miss
when reading. It also keeps scanning t after s runs out (a cheap no-op per character).

Time Complexity: O(n + m)
Space Complexity: O(1)
"""


def append_characters(s: str, t: str) -> int:
    """Return the minimum number of characters to append to s so that t becomes a subsequence of s."""
    remaining = iter(s)
    matched = sum(1 for char in t if char in remaining)
    return len(t) - matched
