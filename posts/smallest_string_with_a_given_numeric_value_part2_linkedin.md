# Two More Ways to Build the Smallest String: Closed Form vs Forward Greedy (Part 2 of 2) 🧮

In Part 1, the right-to-left greedy for **Smallest String With a Given Numeric Value** was correct, plus a validation guard for impossible inputs.

Here are two alternatives.

---

### ✅ Alternative 1: Closed-Form Construction

The answer always has the shape: some 'a's, one middle letter, some 'z's. So compute the three pieces directly.

- Extra points: `k - n`
- Number of 'z's: `extra // 25`
- Middle letter: `'a'` plus `extra % 25`
- Everything left of that (if any) is 'a'

One `divmod`, then three repeated segments joined together. No loop, no index bookkeeping.

The edge case is `k == 26n`. Every letter is 'z', so there is no middle letter and the count of 'a's would go to -1. It needs its own branch.

**Time:** O(n) to build the string, O(1) arithmetic
**Space:** O(n)

---

### ✅ Alternative 2: Forward Greedy With a Feasibility Check

This one reads like the problem statement: build left to right, picking the smallest letter that still lets the rest of the string reach the target.

- With `p` positions still to fill after this one, they can supply at most `26 * p`.
- So the current letter must be at least `remaining - 26 * p`, and at least 1.
- Pick `max(1, remaining - 26 * p)` and move on. No backtracking needed.

It is the same answer by a different argument. Forward greedy proves itself with a feasibility bound, and backward greedy proves itself with an exchange argument.

**Time:** O(n)
**Space:** O(n)

---

### 🧪 How I Tested It

- Both LeetCode examples plus boundaries: n=1, all 'a', all 'z'.
- An exhaustive search of every string for n up to 3, checked against every valid k.
- A separate DP oracle that decides feasibility without using the 26n bound, for n up to 12.
- Cross-checks that all three agree for n up to 1000, with the length, sum, sorted order, and "at most one middle letter" shape verified.
- Large inputs of 100,000 characters at both extremes.
- Invalid inputs must raise `ValueError` in all three.

Everything agreed.

---

### 🎯 Key Takeaways

1. Once you know the shape of the answer, the loop can turn into arithmetic.
2. Two different greedy proofs can land on the same output. Testing them against each other is cheap insurance.
3. The off-by-one lives at the boundary. `k == 26n` was the case that needed special handling.
4. Validate input at the edge, even when the judge promises it is fine.

Do you prefer the loop, the formula, or the forward check? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Greedy #Strings #Math #Testing #Hypothesis #LeetCode #CodingInterview
