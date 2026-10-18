# Take 2, 4, 6... Then Absorb the Leftover: Maximum Split of Positive Even Integers (Part 1 of 2) ➕

**The Problem**:
Given an integer `finalSum`, split it into the **maximum number of unique positive even integers** that add up to it. Return any such split, or an empty list if none exists.

---

### 🧩 Why Brute Force Fails

The number of ways to write a number as a sum of distinct even integers grows very quickly. Searching through them to find the longest is wasteful.
A little structure removes the search entirely.

---

### 🔧 The Greedy Strategy

1. If `finalSum` is odd or not positive, return an empty list. Even numbers can never add up to an odd one.
2. Take the smallest unused even number: 2, then 4, then 6, and so on, as long as it still fits.
3. When the next number no longer fits, there is a leftover that is smaller than that number.
4. Add the leftover to the **largest** number taken so far.

---

### 🧠 Why Is It Optimal?

- **Smallest numbers first means most numbers.** To fit the maximum count of distinct values, use the cheapest ones: 2, 4, 6, ... Any other choice costs at least as much for the same count.
- **The leftover is safe to absorb.** It is even and smaller than the next candidate, so adding it to the last element makes that element bigger than all the earlier ones. Uniqueness holds, and the sum is exact.
- **The count has a clean formula.** The first k even numbers sum to k(k+1), so the answer is the largest k with k(k+1) <= finalSum.

---

### 🔍 Quality Review

The logic was already correct and optimal. Output size is about the square root of `finalSum`, so O(sqrt(n)) time cannot be beaten: you have to write down every element.

Small cleanup:
- The original reduced the parameter `finalSum` itself while looping. I switched to a separate `remaining` variable, so the input is never overwritten and the code reads more clearly.
- A comment now explains why the leftover is safe to add, and why the result is never empty at that point.

I kept the LeetCode parameter name `finalSum` so existing callers do not break.

---

### 📊 Complexity

- **Time:** O(sqrt(finalSum))
- **Space:** O(sqrt(finalSum)) for the output

---

### 🎯 Key Takeaway

For "maximum number of distinct parts", spend the cheapest parts first, then fix the shortfall by enlarging the biggest one.

In Part 2, I look at a closed-form version using `math.isqrt` and a look-ahead loop that never edits an element after placing it.

Where have you seen "triangular numbers" hiding inside a problem? Tell me below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Greedy #Math #LeetCode #CodingInterview
