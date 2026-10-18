# Open the Tap That Reaches Furthest: Minimum Taps to Water a Garden (Part 1 of 2) 🚰

**The Problem**:
A garden runs from 0 to `n` on a line. There are `n + 1` taps at positions 0 through `n`, and tap `i` waters `[i - ranges[i], i + ranges[i]]` when open. Find the **minimum number of taps** to water the whole garden, or -1 if it is impossible.

---

### 🧩 Why Brute Force Fails

Trying every subset of taps is 2^(n+1) options, and n goes up to 10,000. This is a coverage problem in disguise, so a direct strategy should exist.

---

### 🔧 The Greedy Strategy

Turn each tap into an interval, then play a jump game:
1. Compute each tap's interval, clamped to the garden: `[max(0, i - r), min(n, i + r)]`.
2. Sort the intervals by start.
3. Stand at the end of the watered area (start at 0).
4. Among all intervals that start at or before that point, take the one that reaches **furthest**.
5. Count one tap and move to its end.
6. If no interval moves you forward, there is a gap. Return -1.
7. Repeat until the watered area reaches `n`.

---

### 🧠 Why Is It Optimal?

An exchange argument:
- Every interval that starts inside the watered area is a valid next choice.
- The one that reaches furthest leaves the watered area at least as large as any other choice would.
- A larger watered area can only give more options next, never fewer. No other choice can finish with fewer taps.

---

### 📊 Complexity

- **Time:** O(n log n), dominated by the sort
- **Space:** O(n)

---

### 🎯 Key Takeaway

"Minimum number of intervals to cover a range" is almost always the same shape: extend as far as you can from where you stand. Learn it once and you will see it in video clips, taps, jump games and meeting rooms.

In Part 2, I show an O(n) version with no sorting, and a plain DP that makes no greedy assumption.

What other problems have you spotted that are secretly interval cover? Tell me below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Greedy #Intervals #LeetCode #CodingInterview
