# Pack the Lightest First: The Greedy Behind "Apples in a Basket" (Part 1 of 2) 🍎

**The Problem**:
A basket carries at most **5000** units of weight.
Given the weight of each apple, what is the maximum number of apples you can put in it?

---

### 🧩 This Is a Count Problem, Not a Value Problem

You are not maximizing total weight. You are maximizing how many apples you carry.
Every apple counts as **1**, no matter how heavy it is.

So the cheapest apples (in weight) are the best use of the limited capacity.

---

### 🔧 The Greedy Strategy

1. Sort the apple weights in **ascending** order.
2. Add apples one by one while the running total stays $\le$ 5000.
3. Stop at the first apple that does not fit.
4. Return the count.

---

### 🛑 Why Can We Stop at the First Failure?

The list is sorted, so every remaining apple is at least as heavy as the one that just failed.
If this one doesn't fit, none of the later ones will.

---

### 🧠 Why Is It Optimal?

An exchange argument:
- Suppose an optimal basket holds $m$ apples but not the lightest one, $a$.
- Swap any apple in the basket for $a$. The weight can only go down, so the basket is still valid.
- Repeating the swap shows some optimal basket holds the $m$ lightest apples.

If even those $m$ lightest apples don't fit, no set of $m$ apples can.

---

### 🐛 Quality Notes on My First Draft

1. **`weight.sort()` mutates the caller's list.** It passes LeetCode but reorders data the function doesn't own. `sorted()` fixes it.
2. **A magic number: `5000`.** It is the problem's capacity, so it deserves a named constant, or a parameter for reuse.
3. **The `else: break` could be a plain early exit**, which is slightly flatter and easier to read.

The mutation issue is captured in a test marked `xfail(strict=True)`.

---

### 📊 Complexity

- **Time:** O(n log n) for the sort, then a pass that stops early
- **Space:** O(1) auxiliary with the in-place sort

---

### 🎯 Key Takeaway

When you maximize a **count** under a **budget**, spend the budget on the cheapest items first.
The proof is a one-line swap.

In Part 2, we will replace the sort with a **bucket count** and see when that helps, and when it quietly hurts.

What is the simplest greedy problem you have seen that still needed a proof? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Greedy #Sorting #CleanCode #LeetCode #CodingInterview
