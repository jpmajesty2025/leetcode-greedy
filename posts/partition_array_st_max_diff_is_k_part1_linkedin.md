# Subsequences Are a Red Herring: Sort, Then Greedily Cut (Part 1 of 2) ✂️

**The Problem**:
Given an integer array `nums` and an integer `k`, partition `nums` into the fewest subsequences such that, in each one, `max - min <= k`.

What is the minimum number of subsequences?

---

### 🧩 The Word "Subsequence" Is a Distraction

A subsequence keeps the original order, but here **order never affects the answer**.
The only thing that matters is which values end up in the same group.

That means any subset of `nums` is a legal group, so we are free to **sort first**.

---

### 🔧 The Greedy Strategy

After sorting, each group should be a contiguous run of the sorted array:

1. Start a group at the smallest unassigned value, `current_min`.
2. Absorb every value that is $\le$ `current_min + k`.
3. The first value above that limit becomes the next group's `current_min`.
4. Count the groups.

---

### 🧠 Why Is It Optimal?

An exchange argument:
- The smallest value must belong to *some* group, and that group can reach at most `smallest + k`.
- Taking **every** value up to that limit costs nothing, because it only removes work for later groups.
- Any other plan covers a subset of what the greedy group covers, so it needs at least as many groups.

Repeat the argument on what remains, and the greedy count can never be beaten.

---

### 🐛 Two Quality Issues in My First Draft

1. **`nums.sort()` mutates the caller's list.** Passes LeetCode, but reorders data the function doesn't own. `sorted()` fixes it.
2. **`nums[0]` crashes on an empty list.** LeetCode guarantees $n \ge 1$, but real callers might not. Returning 0 is the natural answer.

Tests for both are marked `xfail(strict=True)`, so the suite documents them and will tell me when they are fixed.

---

### 📊 Complexity

- **Time:** O(n log n) for the sort, then one O(n) pass
- **Space:** O(1) auxiliary with the in-place sort (`nums[1:]` quietly allocates O(n) though)

---

### 🎯 Key Takeaway

When a problem says "subsequence" but the constraint ignores order, the sequence is really a **multiset**.
Sort it, then cut greedily.

In Part 2, we will race this against a **presence-array** approach that skips the sort entirely, and see exactly when it wins.

Have you ever been misled by a problem statement's wording? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Greedy #Sorting #CodeReview #LeetCode #CodingInterview
