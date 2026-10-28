# Beating the Sort: A Presence Array Is 3.8x Faster, Until It Isn't (Part 2 of 2) ⚡

In Part 1, we solved Partition Array Such That Maximum Difference Is K by sorting and cutting greedily.

In this scenario, values are bounded by $10^5$. That invites a **Presence Array**:
1. Mark which values occur in a `bytearray` indexed by `value - min`. This is O(n).
2. Scan the value range once, left to right.
3. Start a new group whenever a present value is more than `k` above the group's start.

No comparison sort, and duplicates need no special handling.

More broadly, which one wins?

---

### 💥 The Benchmark (best of 7 runs)

| Workload | Sort | Presence Array | Result |
| :--- | :--- | :--- | :--- |
| 1,000,000 elements, values up to $10^5$ | 260.58 ms | 68.74 ms | **3.79x faster** |
| 100,000 elements, values up to $10^5$ | 15.88 ms | 10.47 ms | 1.52x faster |
| 100,000 identical values | 2.86 ms | 5.23 ms | 1.8x slower |
| 1,000 elements, values up to $10^5$ | 0.09 ms | 3.45 ms | **39x slower** |
| 1,000 elements, values up to $10^9$ | 0.11 ms | ~41,800 ms | **Hopeless** |

---

### 🔍 What the Numbers Really Say

1️⃣ **The cost is O(n + R), not O(n)**:
The scan walks the whole value range $R$, even when it holds few elements.
That is cheap for dense data and wasteful for sparse data.

2️⃣ **Density decides everything**:
With a million elements packed into $10^5$ values, nearly every slot is used.
With a thousand elements, 99% of the scan is wasted.

3️⃣ **The constraint is the algorithm's safety net**:
Raise the value bound to $10^9$ and the array needs about a gigabyte. The benchmark took tens of seconds.
Sorting doesn't care about the value range.

4️⃣ **Python's sort is hard to beat on small inputs**:
It runs in C, and it is nearly linear on data with few distinct values.

---

### 🎯 Key Takeaway

Counting-style tricks trade comparisons for memory proportional to the **value range**.
They win when the range is small relative to the data, and lose when it isn't.
Check the constraints before you reach for them.

Where did a problem's constraints change which algorithm you chose? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Greedy #Sorting #Benchmarking #LeetCode #CodingInterview
