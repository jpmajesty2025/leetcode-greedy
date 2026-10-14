# Lazy Heap vs. Full Sort: Up to 5x Faster, and 3.7x Slower (Part 2 of 2) ⚡

In Part 1, we solved Destroying Asteroids by sorting the asteroids and simulating collisions in ascending order.

Another option is a **Lazy Min-Heap**:
1. Copy the asteroids and `heapify` the copy in O(n).
2. Pop the lightest asteroid and compare it to the planet's mass.
3. Stop as soon as the planet loses.
4. Stop with `True` as soon as `mass >= max(asteroids)`, since nothing can beat the planet anymore.

Both are correct. So which one is faster?

---

### 💥 The Benchmark (500,000 Asteroids)

Best of 7 runs per case, with the sort timed on a fresh copy of the list each run:

| Scenario | Full Sort | Lazy Heap | Result |
| :--- | :--- | :--- | :--- |
| Planet stuck at the first asteroid | 85.18 ms | 21.04 ms | **4.05x faster** |
| Planet heavier than every asteroid | 104.48 ms | 20.13 ms | **5.19x faster** |
| Random asteroids, big planet | 107.76 ms | 23.04 ms | **4.68x faster** |
| All asteroids have mass 1 | 22.62 ms | 14.38 ms | 1.57x faster |
| Must pop nearly everything, then fail | 39.26 ms | 144.41 ms | **3.7x slower** |

---

### 🔍 What Actually Explains the Numbers

1️⃣ **Most wins come from the O(n) early exit, not the heap**:
Computing `max(asteroids)` is a single linear scan.
If the planet already outweighs it, the answer is `True` with no sorting at all.

2️⃣ **Heapify is O(n)**:
Building a heap is cheaper than a full O(n log n) sort, and a stuck planet never pays for the rest.

3️⃣ **Sort is a monster on easy data**:
All-ones input is already sorted, so Python's sort finishes in near-linear time.

4️⃣ **The heap's worst case is real**:
If the planet has to pop almost every asteroid, each pop costs O(log n) in Python-level code.
Sorting runs in C and wins by a wide margin.

---

### 🧪 Verification

Verified with pytest and Hypothesis:
- **Independent Oracle**: Both implementations match a brute-force check over every permutation on small inputs.
- **100% Agreement**: The heap and sort versions return identical answers on random workloads.
- **No Side Effects**: The heap version copies its input, so the caller's list is never reordered.

---

### 🎯 Key Takeaway

A lazy structure only pays off when the early exit actually triggers.
Pick the heap when failures or overwhelming planets are common. Pick the plain sort when you expect to process nearly everything.
Measure on adversarial inputs before choosing.

When did a "smarter" algorithm turn out slower for you? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Heap #PriorityQueue #Benchmarking #Greedy #LeetCode #CodingInterview
