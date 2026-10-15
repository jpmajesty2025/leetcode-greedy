# Sorting vs. Buckets: 3x Faster at Scale, 40,000x Slower When Sparse (Part 2 of 2) ⚖️

In Part 1, Maximum Units on a Truck by sorting box types by units per box.

LeetCode bounds `unitsPerBox` by 1,000. That invites a **Bucket** approach:
1. Add up the number of boxes at each units-per-box value in a list indexed by that value.
2. Scan the buckets from the highest value down.
3. Load boxes until the truck is full.

No comparison sort, and the caller's list is never touched.

Which one wins?

---

### 💥 The Benchmark (best of 7 runs)

| Workload | Sort | Buckets | Result |
| :--- | :--- | :--- | :--- |
| 1,000,000 types, units up to 1,000 | 373.99 ms | 122.40 ms | **3.06x faster** |
| 100,000 types, units up to 1,000 | 28.06 ms | 12.44 ms | 2.26x faster |
| 1,000,000 types, tiny truck | 214.87 ms | 120.58 ms | 1.78x faster |
| 1,000 types (LeetCode's max), units up to 1,000 | 0.129 ms | 0.147 ms | 1.14x slower |
| 1,000 types, units up to $10^6$ | 0.141 ms | 43.37 ms | **~300x slower** |
| 1,000 types, units up to $10^8$ | 0.127 ms | 5,068 ms | **~40,000x slower** |

---

### 🔍 What the Numbers Really Say

1️⃣ **The cost is O(n + U), not O(n)**:
$U$ is the largest units-per-box value. The scan walks every bucket, even the empty ones.

2️⃣ **Bucket wins need lots of data in a small range**:
A million box types share only 1,000 distinct values, so the sort does a lot of redundant comparisons the buckets avoid.

3️⃣ **At LeetCode's actual size, it's a wash**:
With 1,000 box types the sort already finishes in about a tenth of a millisecond.

4️⃣ **The constraint is the safety net**:
Raise the units bound and the bucket list becomes a huge, mostly empty array. The sort doesn't care.

---

### 🧪 Verification

Verified with pytest and Hypothesis, 29 passing tests plus 1 expected failure:
- **Expanded-Box Oracle**: Both versions match "list every physical box, take the best `truckSize`" on small inputs.
- **Exhaustive Oracle**: Both match a search over every possible selection of boxes.
- **Properties**: The result is independent of input order, never exceeds `truck_boxes * max_units`, and a bigger truck never hurts.
- **100% Agreement**: The sort and bucket versions return identical answers across random workloads.

---

### 🎯 Key Takeaway

Counting tricks trade comparisons for memory proportional to the **value range**.
They shine when the range is small and the data is big. At interview-sized inputs, the plain sort is just as fast and far simpler.
Check the constraints before choosing.

Where have constraints changed your choice of algorithm? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Greedy #Sorting #Benchmarking #LeetCode #CodingInterview
