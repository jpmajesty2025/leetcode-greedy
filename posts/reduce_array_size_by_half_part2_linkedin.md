# My O(n) Solution Lost Every Benchmark (Part 2 of 2) 🐌

In Part 1, we solved Reduce Array Size to The Half by counting values and sorting the frequencies in descending order.

The sort costs O(d log d). Frequencies are bounded by $n$, so a **Frequency Bucket** should beat it:
1. Count values with `Counter`.
2. Build a list where slot $f$ holds how many distinct values occur exactly $f$ times.
3. Walk $f$ from $n$ down to 1, taking whole groups at a time with ceiling division.
4. Stop when half the array is removed.

No comparison sort, and it uses $\lceil n/2 \rceil$ so odd lengths are right too.
Strictly O(n). Surely faster?

---

### 💥 The Benchmark (best of 5 runs)

| Workload | Sort | Buckets | Result |
| :--- | :--- | :--- | :--- |
| 10,000 elements (LeetCode's max) | 0.93 ms | 1.24 ms | 1.3x slower |
| 100,000 elements, mostly distinct | 10.16 ms | 12.54 ms | 1.2x slower |
| 1,000,000 elements, 1M range | 247.69 ms | 293.42 ms | 1.2x slower |
| 1,000,000 elements, 1,000 distinct | 48.12 ms | 83.27 ms | 1.7x slower |
| 1,000,000 elements, 10 distinct | 38.96 ms | 70.84 ms | 1.8x slower |
| 1,000,000 elements, skewed | 34.31 ms | 50.91 ms | 1.5x slower |

The "better" algorithm lost **every** time.

---

### 🔍 Why O(n) Lost to O(d log d)

1️⃣ **Counting dominates both versions**:
On 1,000,000 elements, `Counter` alone took about 250 ms.
Sorting the 631,633 counts took about 27 ms, roughly 10% of the work.
The bucket version can only optimize that 10%.

2️⃣ **The sort runs over distinct values, not all elements**:
With few distinct values, there is almost nothing to sort.
The bucket version still allocates an $(n+1)$-slot list and loops over it.

3️⃣ **C beats Python**:
`sorted()` runs in C. The bucket walk and ceiling-division arithmetic run as Python bytecode.

4️⃣ **Ten distinct values is the worst case for buckets**:
The sort has 10 items. The bucket still builds a million-slot list.

---

### 🧪 Verification

Verified with pytest and Hypothesis, 37 passing tests plus 2 expected failures:
- **Exhaustive Oracle**: Both versions match a search over every possible set of values on small inputs.
- **Odd Lengths**: The bucket version matches the oracle for any length. The original is wrong on odd lengths, and a strict `xfail` records it.
- **Properties**: The result is at least 1 and at most the distinct count, independent of input order, and identical in both versions.

---

### 🎯 Key Takeaway

Big-O describes growth, not where the time goes.
Before replacing a step, **measure what share of the runtime it actually has**. I spent my effort on 10% of the problem.

When did profiling change what you chose to optimize? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Greedy #Profiling #Benchmarking #LeetCode #CodingInterview
