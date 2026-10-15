# Delete the Most Frequent Values First: Reduce Array Size to The Half (Part 1 of 2) ✂️

**The Problem**:
You may choose a set of integers and delete **every occurrence** of each one from the array.

What is the smallest set that removes at least half of the elements?

---

### 🧩 Only Frequencies Matter

Choosing a value removes **all** of its copies at once.
So each distinct value is a single item that costs 1 pick and removes `frequency` elements.

The actual numbers don't matter. Only their counts do.

---

### 🔧 The Greedy Strategy

1. Count the frequency of each value with `Counter`.
2. Sort the frequencies in **descending** order.
3. Add them up one at a time, counting picks.
4. Stop as soon as the running total reaches half the array length.

---

### 🧠 Why Is It Optimal?

An exchange argument:
- Every pick costs exactly 1, so we want the most removal per pick.
- If an optimal set uses a value with frequency $f_1$ while skipping a more frequent value with $f_2 > f_1$, swap them.
- The removed total only goes up, so the set is still valid and no larger.

Repeating the swap turns any optimal set into the top-$k$ most frequent values.

---

### 🐛 Three Quality Issues in My First Draft

1. **A stray `self` parameter.** The function is module-level, but it still has a `self` argument copied from LeetCode's class template. Calling `min_set_size(arr)` raises `TypeError`.
2. **`len(arr) // 2` floors for odd lengths.** "At least half" of 3 elements is 2 (1.5 rounded up). The code only asks for 1. LeetCode guarantees even lengths, so the judge never notices, but a ceiling `(n + 1) // 2` is correct for every length.
3. **`import` inside the function**, and a `break` that could be a direct return.

Tests for the first two are marked `xfail(strict=True)`, so the suite documents them and will tell me when they are fixed.

---

### 📊 Complexity

- **Time:** O(n) to count, plus O(d log d) to sort $d$ distinct frequencies
- **Space:** O(d) for the counter

---

### 🎯 Key Takeaway

When one pick removes **all copies** of a value, the problem collapses to "sort the counts".
And if a signature came from a template, check it before you trust it.

In Part 2, we will replace the sort with an **O(n) frequency bucket** version. It looks strictly better on paper, so let's see what the stopwatch says.

Have you ever shipped a function with a leftover `self`? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Greedy #HashMap #CodeReview #LeetCode #CodingInterview
