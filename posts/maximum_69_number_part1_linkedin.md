# Flip the Leftmost 6: The Smallest Greedy Proof You'll Write (Part 1 of 2) 🔢

**The Problem**:
You are given a positive integer made only of the digits 6 and 9.
You may change **at most one** digit (6 becomes 9, or 9 becomes 6).

What is the largest number you can make?

---

### 🧩 What Does One Flip Do?

Changing a digit at place value $p$ changes the number by exactly:
- **+3p** when a 6 becomes a 9
- **-3p** when a 9 becomes a 6

So flipping 9 to 6 can never help. The only useful move is a 6 to 9, or doing nothing.

---

### 🔧 Which 6 Should Flip?

The gain is $3p$, so the **largest place value** wins.
That is the **leftmost** 6.

Why not a lower 6?
- Flipping a 6 at place $q$ gains $3q$. Flipping a higher 6 at place $p > q$ gains $3p$, which is at least $30q$ since places grow tenfold.
- Two flips would be needed to get both gains, and the rules allow only one. Higher always wins.

If there is no 6, the number is already maximal.

---

### 🛠️ The Implementation

A one-liner in Python: convert to a string and replace the first `'6'` with `'9'`.
`str.replace(old, new, 1)` does exactly the "leftmost only" part, and `int()` converts it back.

No loops, no index bookkeeping, no special case for "no 6", because `replace` on a missing character is a no-op.

---

### 🐛 Quality Notes

1. **A space before the parentheses** in the function signature breaks PEP 8 style.
2. **No docstring** explaining that only the leftmost 6 flips.
3. **A hidden limit**: `str(num)` raises for integers beyond 4,300 digits. LeetCode caps this problem at 4 digits, but real code may not.

The third one is captured in a test marked `xfail(strict=True)`.

---

### 📊 Complexity

- **Time:** O(d) where d is the number of digits
- **Space:** O(d) for the string

---

### 🎯 Key Takeaway

Before coding a greedy, ask what a single move is worth.
Here every move has a closed-form value ($\pm 3p$), and the proof falls out in two lines.

In Part 2, we will test an **arithmetic-only** version with no strings at all, and see whether it's worth it.

What is the smallest problem where a greedy proof taught you something? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Greedy #CleanCode #CodeReview #LeetCode #CodingInterview
