# Fixing the Mutation and Trying Heaps: Players and Trainers, Two Alternatives (Part 2 of 2) 🔧

In Part 1, the greedy two-pointer solution for **Maximum Matching of Players With Trainers** was correct and optimal, with one flaw: it sorted the caller's lists in place.

Here are two alternatives I wrote and tested against it.

---

### ✅ Alternative 1: Non-Mutating Sorted Refactor

- Sort **copies** with `sorted()`, so the inputs stay untouched.
- Loop over the sorted trainers once. The number of matches so far doubles as the index of the next waiting player, so the second pointer disappears.
- Break early once every player is matched.

The loop is shorter and the side effect is gone.

**Time:** O(n log n + m log m)
**Space:** O(n + m) for the sorted copies

The cost of the fix is real: O(1) extra space becomes O(n + m). In return, the function has no side effects.

---

### ✅ Alternative 2: Lazy Two-Heap Version

- Heapify copies of both lists in O(n + m).
- Pop the weakest trainer. If it can handle the weakest waiting player, pop that player too and count a match.
- Stop the moment either heap is empty.

**Time:** O(n + m + k log(n + m)), where k is the number of pops actually performed
**Space:** O(n + m)

A heap never orders the whole input, only as much as the loop touches.
That helps when the answer is found early, for example when the players list is tiny.
In the worst case it does about the same work as sorting, with a larger constant factor.

---

### 🧪 How I Tested It

- Known cases: both LeetCode examples, empty sides, exact fits, nobody matching, and 30,000-element inputs.
- A brute-force oracle that tries every assignment on small random inputs.
- Cross-checks that all three versions agree on shuffled large-value inputs.
- Monotonicity: an extra trainer never hurts, and an extra player adds at most one match.
- Mutation checks: both alternatives pass, and the original fails by design as a strict `xfail`.

All three implementations agree on every generated case.

---

### 🎯 Key Takeaways

1. A correct solution can still have a quality flaw. Mutating inputs is one.
2. Fixing a flaw has a price. Here it is extra memory.
3. A heap is not automatically faster than a sort. It only wins when you can stop early.
4. A brute-force oracle plus property tests is the cheapest way to trust a greedy proof.

Do you default to `sorted()` or `.sort()` in your own code? Tell me why below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Greedy #Heap #PriorityQueue #Testing #Hypothesis #LeetCode #CodingInterview
