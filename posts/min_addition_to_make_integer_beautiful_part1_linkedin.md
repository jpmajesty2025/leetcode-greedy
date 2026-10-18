# Round Up to the Next 10, 100, 1000: Minimum Addition to Make Integer Beautiful (Part 1 of 2) 🔟

**The Problem**:
A number is "beautiful" if its digit sum is at most `target`. Given `n` and `target`, find the smallest non-negative `x` such that `n + x` is beautiful.

---

### 🧩 Why Brute Force Fails

Adding 1 at a time and checking each digit sum works for small numbers. But `n` goes up to 10^12, and the answer can be nearly as large as `n` itself, so we cannot count one by one.

---

### 🔧 The Greedy Strategy

Think about what actually shrinks a digit sum: **creating trailing zeros**.
1. If `n` is already beautiful, return 0.
2. Round `n` up to the next multiple of 10. Check the digit sum.
3. Still too big? Round up to the next multiple of 100. Then 1000. And so on.
4. The first rounding that is beautiful gives the answer: the rounded value minus `n`.

It always ends, because rounding up to a power of ten gives a digit sum of 1.

---

### 🧠 Why Is It Optimal?

- **The best answer is `n` rounded up.** Digit sums only drop by creating trailing zeros, so the winner is `n` rounded up to a multiple of some power of ten.
- **Smaller roundings are cheaper.** Rounding up to a multiple of 10 costs at most 9, to a multiple of 100 at most 99, and so on. Trying them in order finds the cheapest one that works.

---

### 🐛 The Bug: A Jump That Overshoots

The step was meant to say "round up to the next multiple of a power of ten". But it takes the remainder against 10 raised to the number's own length. A number is always smaller than that, so the remainder is the number itself, and the step becomes "jump straight to the next power of ten".

The results were valid but not minimal:
- `n = 16, target = 6` returned **84** instead of **4** (16 goes to 20).
- `n = 467, target = 6` returned **533** instead of **33** (467 goes to 500).

Both of those are LeetCode's own examples, so the file would fail them. Cases like 19 or 999 happened to be right, because the nearest good number really was a power of ten.

The fix: round up to a multiple of 10, then 100, then 1000, in turn, and stop at the first beautiful one.

---

### 📊 Complexity

- **Time:** O(d^2) in the number of digits d, because up to d roundings each cost an O(d) digit sum
- **Space:** O(d)

---

### 🎯 Key Takeaway

Passing a few easy examples proves very little. The original was right for 19 and 999 and wrong on both official samples. Always run the problem's own examples first.

In Part 2, I compare two more ways: a quotient trick and a single pass over the digits.

Has a bug ever hidden behind inputs that happened to be right? Tell me below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Greedy #Math #LeetCode #CodingInterview
