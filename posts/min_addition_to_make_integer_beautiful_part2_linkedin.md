# Quotients and Prefixes: Two More Ways to Make an Integer Beautiful (Part 2 of 2) 🧮

In Part 1, the original for **Minimum Addition to Make Integer Beautiful** jumped to the next power of ten instead of the next multiple of 10, 100, and so on. That gave 84 instead of 4 on LeetCode's first example. Here are two alternatives built on the corrected idea.

---

### ✅ Alternative 1: Quotient Digit Sums

Rounding `n` up to a multiple of 10^k gives `ceil(n / 10^k)` followed by k zeros. Trailing zeros add nothing to a digit sum, so we can check the digit sum of the **quotient** alone and never build the large number.

- Try k = 0, 1, 2, ...
- Return `quotient * 10^k - n` for the first quotient whose digit sum fits.

Clean, short, and it reads like the explanation.

**Time:** O(d^2) in the number of digits
**Space:** O(d)

---

### ✅ Alternative 2: Longest Safe Prefix

Work on the digit string in one pass:
- If `n` is already beautiful, return 0.
- Keep the longest prefix of digits whose sum is at most `target - 1`.
- Add 1 to that prefix and replace the remaining digits with zeros.

Why does it work? Adding 1 raises a digit sum by at most 1, and carries only lower it. So the result stays within `target`. An empty prefix gives a power of ten with digit sum 1.

The less obvious part is that this never loses to a clever carry. A carry that "rescues" a longer prefix turns trailing 9s into zeros, which gives exactly the number you would get from a shorter safe prefix. So the longest safe prefix covers it.

**Time:** O(d)
**Space:** O(d)

---

### 🧪 How I Tested It

- LeetCode's three examples, plus 19, 95, 195, 506, 999, 1900, 1999, and exact-digit-sum cases.
- The original's two wrong outputs, 84 and 533, are kept as regression tests.
- A brute force that adds 1 at a time, run on every `n` below 1,500 with seven different targets, and on random `n` up to 20,000.
- Random `n` up to 10^18 and targets up to 162:
  - The result is beautiful.
  - We only add when needed.
  - A non-zero addition always lands on a multiple of 10.
  - The addition is less than the gap to the next power of ten.
  - All three implementations agree.
- A larger target never needs a larger addition.
- Invalid `n` or `target` raises `ValueError`.

The brute-force comparison is my evidence for the "no clever carry beats the safe prefix" argument, on top of the reasoning.

---

### 🎯 Key Takeaways

1. Reduce the number you are checking. The quotient is smaller than the number it represents.
2. When you can reason on digits directly, one pass beats repeated recomputation.
3. Write the proof sketch, then try to break it with brute force.
4. Keep failing outputs from a bug as permanent regression tests.

Which would you code first: the loop, the quotient or the prefix? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Greedy #Math #Testing #Hypothesis #LeetCode #CodingInterview
