# No Sort Needed, and a DP to Check the Greedy: Video Stitching (Part 2 of 2) 🎞️

In Part 1, the sorted greedy for **Video Stitching** was correct, apart from one thing: it sorted the caller's list in place despite its docstring. Here are two alternatives.

---

### ✅ Alternative 1: Furthest-Reach Array

Skip the sort entirely by bucketing clips by their start time.
- Build `reach[s]`, the furthest end of any clip that starts at second `s`, for `s` from 0 to `time`.
- Sweep the seconds once, tracking the furthest point reachable so far.
- Each time the sweep arrives at the end of the covered area, commit to one more clip: the one with the furthest reach.
- If the furthest reach is no further than where you stand, there is a gap, so return -1.

It is the same greedy as before. Bucketing by start time replaces sorting.

**Time:** O(n + time)
**Space:** O(time)

On LeetCode, `time` is at most 100, so this is effectively linear in the number of clips. If `time` were huge and clips few, the sorted version would win instead.

---

### ✅ Alternative 2: Dynamic Programming

Let `dp[t]` be the fewest clips needed to cover [0, t].
- `dp[0] = 0`.
- A clip [s, e] with s < t <= e can finish the cover of [0, t] after the cover of [0, s].
- So `dp[t]` is the minimum of `dp[s] + 1` over such clips.

The answer is `dp[time]`, or -1 if it was never reached.

It is slower, but it makes no greedy argument at all. That makes it a handy independent check on the greedy solutions.

**Time:** O(n * time)
**Space:** O(time)

---

### 🧪 How I Tested It

- All three LeetCode examples, plus a single clip, a clip longer than the event, no clips, a gap at the start, a gap in the middle, touching clips, nested clips, duplicates, and unsorted input.
- A brute force that tries every subset of clips, on random inputs of up to 8 clips with time up to 12. All three implementations matched it.
- Random inputs of up to 30 clips: all three implementations agree, and the answer is -1 or a sensible count.
- Adding a clip never makes things worse.
- A regression test that the input list is not modified. The original fails this on the unfixed code.
- Negative `time` raises `ValueError`. Clips that start before 0 are treated as starting at 0.
- A chain of 100 one-second clips (every clip is needed), and a large input of 200,000 clips.

---

### 🎯 Key Takeaways

1. Replacing a sort with bucketing works when the keys have a small range.
2. A slower, assumption-free DP is a good oracle for a greedy.
3. Fixing a side effect does not change the result. Only a test can show you it was there.
4. Complexity depends on which input is small. Know which limits your problem guarantees.

Would you take the sort or the buckets? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Greedy #DynamicProgramming #Intervals #Testing #Hypothesis #LeetCode #CodingInterview
