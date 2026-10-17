# Two Other Ways to Count the Unmatched Tail: str.find vs a Shared Iterator (Part 2 of 2) 🔎

In Part 1, the one-pass greedy for **Append Characters to String to Make Subsequence** was already correct and optimal. So the alternatives here are about style and constant factors, not big-O.

---

### ✅ Alternative 1: Jump With `str.find`

Instead of stepping through `s` one character at a time, loop over `t`:
- For each character of `t`, ask `s.find(char, position)` for its next occurrence.
- If it is found, move the position just past it.
- If it is not found, the rest of `t` must be appended. Return `len(t) - matched`.

`find` scans in C, so the Python loop runs once per character of `t` instead of once per character of `s`. The total scanning is still at most one pass over `s`.

**Time:** O(n + m)
**Space:** O(1)

The speedup is largest when `s` is long and `t` is short.

---

### ✅ Alternative 2: The Shared Iterator Idiom

- Wrap `s` in one iterator.
- For each character of `t`, test `char in iterator`.
- Count the hits.

Testing membership on an iterator consumes it up to and including the match. After the first miss the iterator is exhausted, so every later test misses as well. That means the hit count is exactly the matched prefix of `t`.

It is a compact trick, but the side effect of `in` is easy to miss, and it keeps looping over `t` after `s` is used up. I would use it knowingly and comment it.

**Time:** O(n + m)
**Space:** O(1)

---

### 🧪 How I Tested It

- All three LeetCode examples plus empty strings, identical strings, order reversals, repeated letters, and late matches.
- An exhaustive brute force that checks every possible suffix length on small random strings.
- A property check that appending the answer really makes `t` a subsequence, and that appending one fewer character does not.
- Monotonicity: extending `s` never hurts, and extending `t` never helps.
- Cross-checks that all three agree on random 26-letter strings, plus 100,000-character inputs.

No disagreements.

---

### 🎯 Key Takeaways

1. When the algorithm is already optimal, the useful questions are about readability and constants.
2. Pushing the inner loop into C, as `find` does, is a legitimate Python optimization.
3. Clever idioms need a comment. If a reader has to know that `in` consumes an iterator, say so.
4. Test the claim "the answer is a suffix of `t`" directly, not just the final number.

Would you ship the iterator one-liner, or keep the explicit loop? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Greedy #Strings #Testing #Hypothesis #LeetCode #CodingInterview
