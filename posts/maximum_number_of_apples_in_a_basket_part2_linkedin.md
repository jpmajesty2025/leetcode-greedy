# Counting Sort vs. Timsort: 2x Faster, 9x Slower, and 4,000x Slower (Part 2 of 2) 🧺

In Part 1, we solved Maximum Number of Apples in a Basket by sorting the weights and packing the lightest first.

Im this problem, every apples weighs at most 1,000. That invites a **Bucket Count**:
1. Count how many apples have each weight, in a list indexed by weight.
2. Walk weights from lightest to heaviest.
3. Take as many apples of that weight as still fit.
4. Stop at the first weight that doesn't fit completely.

No comparison sort, a capacity parameter instead of a magic number, and the caller's list is never touched.

Which one wins?

---

### 💥 The Benchmark (best of 7 runs)

| Workload | Sort | Buckets | Result |
| :--- | :--- | :--- | :--- |
| 1,000,000 apples, weights up to 1,000 | 144.64 ms | 68.15 ms | **2.12x faster** |
| 100,000 apples, weights up to 1,000 | 10.38 ms | 4.92 ms | **2.11x faster** |
| 1,000 apples (LeetCode's max) | 0.062 ms | 0.063 ms | Tie |
| 1,000,000 apples, all weight 1 | 6.50 ms | 58.91 ms | **9x slower** |
| 1,000 apples, weights up to $10^6$ | 0.121 ms | 3.11 ms | **26x slower** |
| 1,000 apples, weights up to $10^8$ | 0.073 ms | 293.52 ms | **~4,000x slower** |

---

### 🔍 What the Numbers Really Say

1️⃣ **The cost is O(n + W), not O(n)**:
$W$ is the heaviest apple. The bucket list has $W + 1$ slots, even when almost all are empty.

2️⃣ **Random data is where buckets win**:
A million apples spread over 1,000 weights makes the sort do a lot of comparison work the counting loop avoids.

3️⃣ **Timsort loves easy data**:
A million identical weights is already "sorted", so Python's sort finishes almost instantly.
The bucket version still pays a Python-level loop iteration for each apple.

4️⃣ **At LeetCode's size, it's a draw**:
With at most 1,000 apples both finish in about a twentieth of a millisecond.

---

### 🧪 Verification

Verified with pytest and Hypothesis, 43 passing tests plus 1 expected failure:
- **Exhaustive Oracle**: Both versions match a search over every subset of apples on small inputs.
- **Capacity Oracle**: The bucket version matches the same search for arbitrary capacities.
- **Properties**: The chosen apples really fit, one more apple would not, and the result is independent of input order.
- **100% Agreement**: The sort and bucket versions return identical answers across random workloads.

---

### 🎯 Key Takeaway

Counting tricks trade comparisons for memory proportional to the **value range**, and Python-level loops are slow.
They win on large random data with a small range, and lose on sorted data or a wide range.
Measure before you choose.

When did the "clever" algorithm lose to a built-in for you? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Greedy #Sorting #Benchmarking #LeetCode #CodingInterview
