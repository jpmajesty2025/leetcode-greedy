# Cut Only When You Must: Optimal Partition of a String (Part 1 of 2) ✂️

**The Problem**:
Split a string into the **fewest** substrings such that no letter appears twice within any single substring. Every character belongs to exactly one piece.

---

### 🧩 Why Brute Force Fails

Between any two neighbouring characters you can cut or not cut, so a string of length n has 2^(n-1) possible partitions.
With n up to 10^5, checking them all is out of the question.

---

### 🔧 The Greedy Strategy

1. Keep a set of the letters in the current substring.
2. Walk the string left to right.
3. If the next letter is already in the set, we **must** cut before it. Count a new substring and clear the set.
4. Add the letter to the set.
5. Return the count, starting from 1 for the first piece.

---

### 🧠 Why Is It Optimal?

An exchange argument:
- Suppose an optimal partition cuts earlier than the greedy one does. Moving that cut to the right, to the latest legal spot, keeps both pieces valid. The right piece only gets shorter, and a shorter piece cannot gain a repeat.
- So extending each piece as far as it can go never hurts, and the greedy choice of "cut only when forced" matches the best possible count.

A useful sanity bound: each piece holds at most 26 distinct lowercase letters, so the answer is at least `ceil(n / 26)`.

---

### 🐛 One Real Bug

The function was declared as `partition_string(self, s)` but lives at module level, a leftover from pasting a LeetCode class method.
Calling `partition_string("abc")` raises `TypeError: missing 1 required positional argument`.

Removing `self` fixes it. The algorithm itself needed no change.

I also documented one edge case: an empty string returns 1. The problem wants "one or more substrings" and guarantees a non-empty input, so I left that behavior and wrote it down.

---

### 📊 Complexity

- **Time:** O(n)
- **Space:** O(1), since the set holds at most 26 letters

---

### 🎯 Key Takeaway

When a rule forces a cut ("no repeats"), delay the cut until it is forced. Lazy cutting is often exactly optimal.

And always call your function once, the way a user would. A signature copied from a class would have failed on the first run.

In Part 2, I compare a bitmask and a last-seen-index version.

What is the sneakiest copy-paste bug you have shipped? Tell me below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Greedy #Strings #LeetCode #CodingInterview
