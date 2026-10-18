# Always Extend as Far as You Can: Video Stitching (Part 1 of 2) 🎬

**The Problem**:
You have video clips, each with a start and end time, and an event that lasts `time` seconds. Clips may overlap and can be cut freely. Find the **fewest clips** that cover the whole event from 0 to `time`, or return -1 if that is impossible.

---

### 🧩 Why Brute Force Fails

Trying every subset of clips is 2^n possibilities, and you still have to check coverage for each one. This is really an interval-cover problem, so there should be a direct strategy.

---

### 🔧 The Greedy Strategy

It plays out like a jump game:
1. Sort the clips by start time.
2. Stand at the end of the covered area (start with 0).
3. Among all clips that start at or before that point, find the one that reaches **furthest**.
4. Take it. Count one clip and move to its end.
5. If no clip moves you forward, there is a gap. Return -1.
6. Repeat until the covered area reaches `time`.

---

### 🧠 Why Is It Optimal?

An exchange argument:
- At any point, every clip that starts inside the covered area is a valid next choice.
- Choosing the one that reaches furthest leaves the covered area at least as large as any alternative would.
- A larger covered area can only offer more options next, never fewer. So no other choice can finish with fewer clips.

---

### 🐛 The Quality Bug: A Docstring That Lies

The docstring promised "The input is not modified". But the code called `clips.sort(...)`, which reorders the caller's list in place.

I confirmed it: passing `[[5, 10], [0, 2], [1, 5]]` came back as `[[0, 2], [1, 5], [5, 10]]`.

That is a nasty kind of bug. The result is correct, so nothing fails right away. But anyone who relies on the list order afterwards gets surprised.

The fix is to sort a copy with `sorted(...)`. I also dropped the secondary sort key on end time, since taking the maximum end already handles ties. And a negative `time` now raises a clear `ValueError`.

---

### 📊 Complexity

- **Time:** O(n log n), dominated by the sort
- **Space:** O(n) for the sorted copy

---

### 🎯 Key Takeaway

Read your docstring as a promise and test it. "Does not modify the input" is easy to write and easy to break.

In Part 2, I compare an O(n + time) version with no sorting, and a plain DP that makes no greedy assumption.

Which side effects have caught you off guard? Tell me below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Greedy #Intervals #LeetCode #CodingInterview
