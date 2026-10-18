# Counting Bits Instead of Looping: Two More Ways to Reach the Target (Part 2 of 2) 🔢

In Part 1, the backward greedy for **Minimum Moves to Reach Target Score** was correct, but it looped a billion times when `maxDoubles` was 0. Here are two alternatives that stay fast in every case.

---

### ✅ Alternative 1: Bit-Counting Closed Form

Look at what the backward greedy does to the binary form of `target`:
- Halving is a right shift. It costs one move.
- An odd number needs one extra subtraction first. That happens exactly when the lowest bit is a 1.

So after halving `d` times, the total cost is:
- `d` moves for the halvings,
- plus the number of 1-bits among the low `d` bits of `target`,
- plus `(target >> d) - 1` increments to get what is left down to 1.

The number of useful doubles is `d = min(maxDoubles, bit_length - 1)`. Extra doubles would push below 1, so they are never used.

No loop at all, just a shift, a mask and a bit count.

**Time:** O(log target) for the bit operations
**Space:** O(1)

---

### ✅ Alternative 2: Bulk-Step Loop

Keep a loop, but handle each halving in one step:
- While doubles remain and the target is above 1, add `1 + (target % 2)` to the count and halve.
- When the loop ends, add `target - 1` for the remaining increments.

This is the original idea with the odd-number fix merged into the halving step. It runs at most about log2(target) iterations, whatever the inputs.

**Time:** O(log target)
**Space:** O(1)

---

### 🧪 How I Tested It

- All three LeetCode examples, plus 1, 2, 3, 4, 7, 8, 15 and 16, and cases where extra doubles go unused.
- A forward breadth-first search over (value, doubles used) as an independent oracle, on random targets up to 80 with up to 8 doubles.
- Random targets up to 10^9 and doubles up to 100: all three agree, and the answer lies between `log2(target)` and `target - 1`.
- A timing test: `target = 10^9` with zero doubles must finish well under a second.
- Targets below 1 and negative `maxDoubles` raise `ValueError`.
- More doubles never hurt, and the next target costs at most one move more.

One of my own properties was false. I asserted that a larger target never costs fewer moves, and Hypothesis found a counterexample at once: with two doubles, 7 costs 4 moves but 8 costs 3. The code was right and my claim was wrong. I replaced it and kept the counterexample as its own test.

---

### 🎯 Key Takeaways

1. Reading an algorithm in binary can turn a loop into a formula.
2. An oracle built a different way, here searching forward, is worth more than examples written by the same mind.
3. Property tests also test your assumptions. When one fails, check whether the code or the claim is wrong.

Do you reach for a formula or a loop first? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Greedy #BitManipulation #Testing #Hypothesis #LeetCode #CodingInterview
