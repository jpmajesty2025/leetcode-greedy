# Counting Sort vs. sorted(): The Winner Depends on the Shape of the Data (Part 2 of 2) 📊

In Part 1, we solved Maximum Ice Cream Bars with the counting sort the problem hints at.

I benchmarked three versions:
1. **Original**: counting sort, bars bought one at a time, no early exit.
2. **Refactored Counting**: one `min(count, coins // price)` step per price, and it stops once a price group can't be fully afforded.
3. **Sorted**: `sorted(costs)` plus a cheapest-first loop, with no assumptions about the price range.

All three return identical answers on every test.

---

### 💥 The Benchmark (best of 5 runs, milliseconds)

| Workload | Original | Counting | Sorted |
| :--- | :--- | :--- | :--- |
| 1,000 bars (LeetCode's max), coins $10^4$ | 3.60 | 0.38 | **0.05** |
| 100,000 bars, coins $10^5$ | 9.72 | **4.70** | 11.66 |
| 1,000,000 bars, coins $10^5$ | 53.25 | **48.81** | 196.52 |
| 1,000,000 bars, buys everything | 97.63 | **57.34** | 236.24 |
| 999 cheap bars plus one priced $10^7$ | 412.17 | 30.11 | **0.05** |

---

### 🔍 What the Numbers Really Say

1️⃣ **At LeetCode's size, `sorted()` wins**:
With 1,000 bars, the counting versions pay to allocate and scan a price array. Sorting 1,000 integers takes about 50 microseconds.

2️⃣ **At scale, counting wins**:
A million bars over $10^5$ prices is where skipping comparison sorting pays off: roughly 4x faster than `sorted()`.

3️⃣ **The original's missing early exit is expensive**:
With one outlier priced at $10^7$, it scanned ten million empty slots after the coins were gone. That's 412 ms for a 1,000-element input.
The refactor stops at the first group it can't afford, but it still allocates the array.

4️⃣ **Sparse prices break counting entirely**:
`sorted()` doesn't care that a price is $10^7$, or $10^12$. A counting array would need that many slots.

---

### 🧪 Verification

Verified with pytest and Hypothesis, 53 passing tests plus 1 expected failure:
- **Exhaustive Oracle**: All three match a search over every subset of bars on small inputs.
- **Independent Oracle**: All three match a cheapest-first running-sum check on larger random inputs, in any order.
- **Properties**: The result never exceeds the number of bars, and more coins never buys fewer.
- **Edge Cases**: Free bars, exact change, huge prices, and unaffordable bars.

---

### 🎯 Key Takeaway

There's no universally fastest sort.
Counting sort wins when the data is large and the value range is small. Plain `sorted()` wins when the data is small or the range is wide.
Look at the constraints, then measure.

What's the biggest input-shape surprise a benchmark has given you? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Greedy #CountingSort #Benchmarking #LeetCode #CodingInterview
