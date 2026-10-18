# Skip the Sort, or Skip the Greedy: Two More Ways to Water the Garden (Part 2 of 2) 💧

In Part 1, the sorted greedy for **Minimum Number of Taps to Open to Water a Garden** was correct and clean, with one small fix for negative ranges. Here are two alternatives.

---

### ✅ Alternative 1: Furthest-Reach Array (O(n))

Tap positions and reaches are integers, so every interval's left end is an integer from 0 to `n`. That lets you bucket instead of sorting.
- Build `reach[left]`: the furthest right end among taps starting exactly at `left`.
- Sweep positions 0 to `n - 1` once, tracking the furthest point any tap seen so far can reach.
- When the sweep arrives at the end of the watered area, open one more tap: the furthest one.
- If it goes no further than where you are, there is a gap, so return -1.

Same greedy, with the sort replaced by bucketing.

**Time:** O(n)
**Space:** O(n)

---

### ✅ Alternative 2: Dynamic Programming

Let `dp[j]` be the fewest taps needed to water `[0, j]`.
- `dp[0] = 0`, everything else starts as unreachable.
- Process taps by left end. A tap `[left, right]` can finish the job for every point in `(left, right]`, after `[0, left]` is watered: `dp[j] = min(dp[j], dp[left] + 1)`.
- The answer is `dp[n]`, or -1 if still unreachable.

It is slower, but it makes no greedy argument at all, which makes it a useful independent check on the greedy versions.

**Time:** O(n times the tap range)
**Space:** O(n)

One typing detail: I used an integer for "unreachable" instead of infinity, so the table stays a list of ints and the return type stays honest.

---

### 🧪 How I Tested It

- Both LeetCode examples, plus an empty garden, one tap at each end, touching intervals that meet at a single point, gaps in the middle, and taps with ranges bigger than the garden.
- A brute force that tries every subset of taps, on random gardens up to length 8. All three implementations matched it.
- Random gardens up to length 60: all three agree and results are in range.
- Making any tap's range bigger never hurts.
- The input is left unmodified. A wrong length, negative `n` and negative ranges raise `ValueError`.
- Scale checks: a 10,000-length garden with one huge tap, a pattern where exactly `n/2 + 1` taps are needed, and a DP-vs-greedy comparison on a moderate input.

---

### 🎯 Key Takeaways

1. When keys are small integers, bucketing replaces sorting.
2. A DP with no greedy assumption is a good oracle for a greedy.
3. Touching intervals count as covering. Test that boundary on purpose.
4. Start from the pattern you know. Here the video-stitching solution transferred almost line for line.

Would you code the sort, the buckets or the DP first? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Greedy #DynamicProgramming #Intervals #Testing #Hypothesis #LeetCode #CodingInterview
