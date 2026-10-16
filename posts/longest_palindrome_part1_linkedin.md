# You Never Build the Palindrome: Counting Letters for the Longest One (Part 1 of 2) 🔤

**The Problem**:
Given a string of lowercase and uppercase letters, what is the length of the longest palindrome you can build from its letters?
Each letter can be used as often as it appears, and case matters ("A" and "a" are different).

---

### 🧩 What Does a Palindrome Need?

A palindrome reads the same in both directions, so its letters come in **mirrored pairs**.
At most one letter can sit alone in the middle.

So the problem is not about order at all. It is about **how many pairs** the letters can form.

---

### 🔧 The Counting Strategy

1. Count how many times each letter appears.
2. A letter seen $f$ times contributes $f$ if $f$ is even, or $f - 1$ if $f$ is odd.
3. If **any** letter had an odd count, add 1 for the center.

You never construct the string. You only add up lengths.

---

### 🧠 Why Is This Optimal?

- Pairs: each letter can supply $\lfloor f/2 \rfloor$ mirrored pairs, and no letter can supply more.
- Center: only one unpaired letter fits in the middle, so extra leftover letters from other odd counts are wasted.
- If two letters both have odd counts, we still only use one extra letter in total.

That gives the upper bound, and the counting strategy reaches it.

---

### 📊 Complexity

- **Time:** O(n) to count
- **Space:** O(k) where $k$ is the number of distinct characters (at most 52 for letters)

---

### 🎯 Key Takeaway

When a problem asks for the best structure you could *build*, check whether you need to build it at all.
Here the answer is pure arithmetic on letter counts.

In Part 2, I race `Counter` against a set-toggling trick and a `str.count` approach. The winner depends on how many distinct characters there are.

What problem did you solve by *not* building the thing it asked for? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Greedy #HashMap #Strings #LeetCode #CodingInterview
