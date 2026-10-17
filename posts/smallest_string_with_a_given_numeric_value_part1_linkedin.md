# Fill With 'a', Then Push the Weight to the Right: Smallest String With a Given Numeric Value (Part 1 of 2) 🔤

**The Problem**:
Each lowercase letter has a value: a=1, b=2, ... z=26.
Given a length `n` and a target `k`, return the **lexicographically smallest** string of length `n` whose letter values sum to `k`.

---

### 🧩 Why Brute Force Fails

There are 26^n strings of length n. Even for n = 10 that is over 141 trillion candidates, and the limit is 10^5.

---

### 🔧 The Greedy Strategy (Build From the Right)

1. Start with a string of n 'a's. That uses n points, leaving `k - n` extra.
2. Walk from the **last** position backwards.
3. At each position, add as much as the letter can take: `min(25, remaining)`.
4. Stop when the extra points run out.

The result looks like `aaa...a [one middle letter] zzz...z`.

---

### 🧠 Why Is It Optimal?

Lexicographic order is decided by the earliest differing character, so earlier positions matter most.
- Any extra point placed on an early letter makes that letter larger, and the string larger.
- So every point should sit as far right as possible.
- The rightmost letter can absorb 25 extra points before it hits 'z', then the next one, and so on.

Pushing weight right keeps the left side as small as possible. Because the sum is fixed, the left side cannot be any smaller.

---

### 🐛 One Quality Issue: Silent Garbage on Bad Input

LeetCode guarantees `n <= k <= 26n`. But what if a caller breaks that?
- If `k > 26n`, the index keeps decreasing past zero. Python's negative indexing wraps around and quietly overwrites letters at the end. You get a wrong string with no error.
- If `k < n`, the loop never runs and you get n 'a's, which has the wrong numeric value.

The fix is a one-line guard that raises `ValueError` when `k` is outside `n..26n`. Valid inputs behave exactly as before.

I checked the algorithm itself against an exhaustive search of all 26^n strings for n up to 3. It was correct everywhere it should be.

---

### 📊 Complexity

- **Time:** O(n)
- **Space:** O(n) for the result

---

### 🎯 Key Takeaway

For "smallest string" problems, ask which positions matter most, then keep those as small as possible and dump the excess on the least important end.

In Part 2, I look at a closed-form version with no loop and a left-to-right greedy that reads like the problem statement.

Have you ever been bitten by Python's negative indexing? Tell me below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Greedy #Strings #LeetCode #CodingInterview
