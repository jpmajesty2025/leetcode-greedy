# Cheapest First, Counted Not Sorted: Ice Cream Bars with Counting Sort (Part 1 of 2) 🍦

**The Problem**:
You have `coins` to spend and a list of ice cream bar prices.
You can buy bars in any order. What is the maximum number of bars you can afford?

---

### 🧩 Why Cheapest First Is Optimal

Every bar counts as **1**, whatever it costs.
So cheaper bars are strictly better use of the same coins.

An exchange argument:
- Suppose an optimal purchase skips a cheap bar but buys a pricier one.
- Swap them. The cost can only go down, so the purchase is still affordable.
- Repeat, and the optimal purchase becomes "the $k$ cheapest bars".

---

### 🔧 The Counting Sort Approach

Prices are bounded by $10^5$, so we can skip comparison sorting:
1. Build an array where slot $p$ holds how many bars cost exactly $p$.
2. Walk $p$ upward from the cheapest price.
3. Buy bars at that price while coins last.

The array index *is* the sorted order.

---

### 📊 Complexity

- **Time:** O(n + C) where C is the largest price
- **Space:** O(C) for the frequency array

---

### 🎯 Key Takeaway

When values live in a small known range, the array index can *be* the sort.
But "O(n + C)" only holds if you stop scanning when the work is done.

In Part 2, we'll benchmark the original counting sort, and a plain `sorted()` version. The ranking changes with the input.

Have you ever used counting sort in a real project? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Greedy #CountingSort #CodeReview #LeetCode #CodingInterview
