# Match Greedily, Append the Rest: Append Characters to String to Make Subsequence (Part 1 of 2) 🧵

**The Problem**:
Given two lowercase strings `s` and `t`, return the minimum number of characters to **append to the end of `s`** so that `t` becomes a subsequence of `s`.

---

### 🧩 Why Brute Force Fails

Trying every possible string to append is exponential. Even checking "is t a subsequence of s plus this suffix" for each candidate is wasteful.
Both strings can be 10^5 long, so we need one linear pass.

---

### 🔧 The Greedy Strategy

1. Keep a pointer into `t`: the next character we still need to find.
2. Scan `s` once, left to right.
3. Whenever the current character of `s` equals the needed character of `t`, advance the `t` pointer.
4. After the scan, everything in `t` from the pointer onward is unmatched.
5. Return `len(t) - pointer`.

---

### 🧠 Why Is It Optimal?

Two observations:
- **Matching each character as early as possible is never worse.** Taking the earliest occurrence leaves the longest remaining stretch of `s` for the rest of `t`. This is the standard exchange argument for subsequences.
- **The best suffix to append is the unmatched tail of `t`.** We only add characters at the end, so whatever prefix of `t` we matched in `s` stays. The remaining part of `t` must be appended in order, and nothing shorter works.

So the answer is the length of `t` minus the longest prefix of `t` that already fits inside `s`.

---

### 🔍 Quality Review

This one was already correct and optimal: O(n + m) time and O(1) space, with no input mutation.

My small refactor:
- Replace the two-index `while` loop with a `for` over the characters of `s`.
- Stop as soon as the whole of `t` has matched.
- Name the pointer `matched`, since it is the length of the matched prefix of `t`.

Same behavior, one less index to keep track of.

---

### 📊 Complexity

- **Time:** O(n + m)
- **Space:** O(1)

---

### 🎯 Key Takeaway

"Is A a subsequence of B" is almost always a single greedy pass with one pointer. Extending that to "how much is left over" just means reading the pointer at the end.

In Part 2, I compare two alternatives: one that jumps with `str.find`, and a clever one-liner with a shared iterator.

What is the shortest subsequence trick you know? Tell me below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Greedy #TwoPointers #Strings #LeetCode #CodingInterview
