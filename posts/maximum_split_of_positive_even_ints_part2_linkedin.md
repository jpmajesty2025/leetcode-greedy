# Closed Form vs Look-Ahead: Two More Ways to Split Into Even Integers (Part 2 of 2) 🧮

In Part 1, the greedy for **Maximum Split of Positive Even Integers** was already correct and optimal. These alternatives differ in how they find the count and how they handle the leftover.

---

### ✅ Alternative 1: Closed-Form Count With `math.isqrt`

Halve everything: splitting `finalSum` into distinct evens is the same as splitting `finalSum / 2` into distinct positive integers.
- Using 1 through k costs k(k+1)/2.
- So the best count k is the largest value with k(k+1)/2 <= half.
- Solve it directly with `(isqrt(8 * half + 1) - 1) // 2`.

Then build 2, 4, ..., 2k with a single `range()` and add the leftover to the last element.

The nice part is that `isqrt` works in exact integer arithmetic. A floating-point `sqrt` can be off by one for large inputs. This version finds the count in O(1) time.

**Time:** O(sqrt(n)) to build the output, O(1) to find k
**Space:** O(sqrt(n))

---

### ✅ Alternative 2: Look-Ahead Greedy

The original appends numbers and then edits the last one at the end. This version avoids editing:
- Take the candidate only if nothing remains after it, or what remains is larger than the candidate.
- Otherwise append all of the remaining sum as the final element, and stop.

Every element is decided once and never changed. The loop does a little more checking per step, in exchange for no fix-up after it.

**Time:** O(sqrt(n))
**Space:** O(sqrt(n))

---

### 🧪 How I Tested It

- LeetCode examples (12, 7, 28), plus 2, 4, 6, 8, 10 and 30. The number 30 is the exact triangular case with no leftover.
- Exact outputs for small values, such as `[2, 4, 6, 16]` for 28.
- An exhaustive recursive search for the maximum count on every even sum up to 120. Each result must also be a valid split.
- Property tests on random values up to a million, including negatives:
  - Odd or non-positive inputs give an empty list.
  - Parts are positive, even, unique and sum to the input.
  - The count equals the independent `isqrt` formula.
  - All three implementations return the same list.
- The count grows by at most one when the sum increases by 2.
- A 10^10 input, checking that k parts fit and k + 1 would not.

---

### 🎯 Key Takeaways

1. Converting a problem into a simpler one, here by halving, often exposes a formula.
2. Use `math.isqrt` instead of `int(sqrt(...))` when exactness matters.
3. A look-ahead check can replace a repair step after the loop.
4. The output size sets the lower bound, so a formula for the count helps clarity, not big-O.

Do you prefer fixing things up afterward or deciding right the first time? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Greedy #Math #Testing #Hypothesis #LeetCode #CodingInterview
