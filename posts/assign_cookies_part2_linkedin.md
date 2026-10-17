# Sort or Heap? The Lazy Version Won Exactly Once (Part 2 of 2) 🍪

In Part 1, we solved Assign Cookies with sort plus two pointers.

I benchmarked three versions:
1. **Original**: `g.sort()` and `s.sort()` in place, then a `while` loop with two indices.
2. **Refactor**: `sorted()` copies, so the inputs are untouched, then a plain `for` over the cookies that stops when every child is content.
3. **Lazy Two-Heap**: `heapify` copies of both lists in O(n + m), then pop one cookie at a time and match it against the least greedy child.

All three return identical answers on every test.

---

### 💥 The Benchmark (best of 3 runs, milliseconds)

| Workload | Original | Refactor | Two-Heap |
| :--- | :--- | :--- | :--- |
| 30,000 × 30,000 (LeetCode's max) | 16.3 | **14.2** | 21.8 |
| 1M × 1M, random | 1,313 | **1,067** | 3,829 |
| 1M × 1M, already sorted | 572 | **463** | 1,616 |
| 10 children, 1M cookies | 529 | **405** | 1,070 |
| 1M children, 10 cookies | 330 | 319 | **41** |

---

### 🔍 What the Numbers Really Say

1️⃣ **The non-mutating refactor is not slower**:
It is 3 to 23% faster than the in-place original, depending on the input. A `for` loop over the cookies does less work per step than a `while` with two index checks and `len()` calls.
Fixing the mutation did not cost speed here.

2️⃣ **The heap loses almost everywhere**:
Each pop is O(log n) and runs through Python-level code. Timsort runs in C, and on already-sorted input it is nearly linear.

3️⃣ **The one heap win is early exit**:
With 1M children and just 10 cookies, the heap stops after about 10 pops, and `heapify` is O(n) instead of O(n log n). That's about 8x faster.

4️⃣ **Lazy only pays when the work really ends early**:
"Stop when cookies run out" is a rare shape for real inputs. The sort is the safer default.

---

### 🧪 Verification

Verified with pytest and Hypothesis, 58 passing tests plus 1 expected failure:
- **Brute-Force Oracle**: All three match an exhaustive search over every assignment on small inputs.
- **Properties**: Shuffling either list changes nothing, the result never exceeds `min(children, cookies)`, an extra cookie never hurts, and an extra child adds at most one content child.
- **100% Agreement**: All three implementations return identical answers, including at 32-bit maximum values.

---

### 🎯 Key Takeaway

Fix the side effects first, and measure afterward. Here the safer code was also slightly faster.
Reach for a heap when you can stop early, not just because heaps feel smarter.

Which "obvious" optimization has a benchmark disproved for you? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Greedy #Heap #Benchmarking #LeetCode #CodingInterview
