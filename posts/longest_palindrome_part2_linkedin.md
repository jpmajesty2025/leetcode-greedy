# Counter vs. Set-Toggle vs. str.count: The Winner Flips With Distinct Characters (Part 2 of 2) 🏁

In Part 1, we solved finding the longest palindrome from a given string by counting letters with `Counter`.

I raced it against two alternatives:
1. **Set-Toggle**: walk the string once, adding a character to a set if absent and removing it if present. At the end the set holds the characters with odd counts, and the answer is `len(s) - len(odd) + 1` (or `len(s)` if none).
2. **Per-Character `str.count`**: take `set(s)` and ask C-level `str.count` for each distinct character.

All three agree on every test.

---

### 💥 The Benchmark (best of 5 runs, milliseconds)

| Workload | Counter | Set-Toggle | `str.count` |
| :--- | :--- | :--- | :--- |
| 2,000 letters (LeetCode's max) | **0.060** | 0.106 | 0.068 |
| 1M characters, 52 letters | 39.19 | 57.02 | **33.30** |
| 1M characters, 2 distinct | 41.84 | 53.99 | **12.74** |
| 1M characters, 1 distinct | 41.57 | 49.92 | **5.85** |
| 1M characters, 5,000 distinct | **73.29** | 121.99 | 1,508.80 |

---

### 🔍 What the Numbers Really Say

1️⃣ **`str.count` is O(n × k)**:
Each call scans the entire string. With 1 or 2 distinct characters that is almost free, about 7x faster than `Counter`.
With 5,000 distinct characters it scans a million characters 5,000 times: about 20x slower.

2️⃣ **Set-Toggle is clever but never wins**:
It does one pass, but each step runs a Python-level membership check and add/remove. `Counter` does the whole count in C.

3️⃣ **`Counter` is the safe default**:
It is never best by a large margin, and never terrible. It stays close to the best option from 1 to 5,000 distinct characters.

4️⃣ **At LeetCode's size, nothing matters**:
All three finish in about a tenth of a millisecond.

---

### 🧪 Verification

Verified with pytest and Hypothesis, 58 passing tests:
- **Brute-Force Oracle**: All three match an exhaustive search over every sub-multiset and every arrangement on small strings.
- **Properties**: Anagrams give the same answer, the result equals `len(s) - max(odd_letters - 1, 0)`, its parity matches having a center, and appending characters never shortens it.
- **100% Agreement**: All three return identical answers across random strings.

---

### 🎯 Key Takeaway

"Clever" Python-level tricks lose to C-level built-ins more often than the Big-O suggests.
A complexity of O(n × k) can still be the best choice when $k$ is known to be tiny.
When $k$ is unbounded, it is not.

Which built-in has surprised you by beating a cleverer hand-written loop? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Strings #HashMap #Benchmarking #LeetCode #CodingInterview
