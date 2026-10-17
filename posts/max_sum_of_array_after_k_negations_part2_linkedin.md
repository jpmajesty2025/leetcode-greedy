# Sort, Heap, or Counting? It Depends How Many Numbers Are Negative (Part 2 of 2) ⚖️

In Part 1, we solved Maximize Sum Of Array After K Negations by sorting a copy, flipping negatives, and using parity for the rest.

I benchmarked three versions:
1. **Sorted**: sorted copy, flip the negatives, `min()` for the leftover.
2. **Heap**: heapify a copy, then repeatedly pop the smallest, negate it, and push it back.
3. **Counting**: bucket the values (LeetCode's range is -100 to 100), flip whole buckets at once.

None of them touches the caller's list, and all three return identical answers on every test.

---

### 💥 The Benchmark (best of 3 runs, milliseconds)

| Workload | Sorted | Heap | Counting |
| :--- | :--- | :--- | :--- |
| 10,000 numbers (LeetCode's max) | 2.1 | 1.9 | **1.4** |
| 1M, large k, values -100..100 | 195 | 356 | **184** |
| 1M, small k | 115 | **54** | 174 |
| 1M, mostly negative, large k | 171 | 526 | **159** |
| 1M, all positive | 111 | **32** | 145 |
| 1M, small k, values up to $10^9$ | 225 | **47** | not applicable |

---

### 🔍 What the Numbers Really Say

1️⃣ **The heap wins when few flips matter**:
`heapify` is O(n) and runs in C. With a small $k$, or no negatives at all, the heap does about one or two pops. That's 2 to 5x faster than sorting.

2️⃣ **The heap loses when many negatives need flipping**:
Every negative costs a pop and a push through Python-level code. With 1M mostly negative numbers it was about 3x slower than sorting.

3️⃣ **Counting is modestly faster, not magically linear**:
Its counting loop runs in Python. It beat the sort by only 6 to 7% when $k$ was large, and lost to it when $k$ was small.

4️⃣ **Counting needs a bounded range**:
At values up to $10^9$ the bucket array would be enormous. The sort and heap don't care.

5️⃣ **At LeetCode's size, nothing matters**:
Everything finishes in a couple of milliseconds.

---

### 🧪 Verification

Verified with pytest and Hypothesis, 68 passing tests:
- **Brute-Force Oracle**: All three match an exhaustive search over every sequence of $k$ flips on small inputs.
- **Properties**: Shuffling the input changes nothing, the result is bounded by the sum of absolute values, its parity matches the input sum's, and $k$ and $k+2$ agree once the negatives are gone.
- **No Side Effects**: Each version leaves the input list untouched.

---

### 🎯 Key Takeaway

Pick the data structure by the shape of the input.
Heaps shine when the work ends early. Sorting is the safe default. Counting helps only when the value range is small.

When did the shape of your data change your algorithm choice? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Greedy #Heap #Benchmarking #LeetCode #CodingInterview
