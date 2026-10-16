# Count First, Match Later: Why a Single Pass Was 6x Slower (Part 2 of 2) 🏎️

In Part 1, we found a bug in a solution to Longest Palindrome by Concatenating Two-Letter Words and fixed it by counting words and pairing each mirror set exactly once.

There is a natural alternative: a **Streaming Matcher**.
1. Walk the words once.
2. If the current word's reverse is waiting, consume it and add 4 letters.
3. Otherwise put the word in a waiting pool.
4. At the end, if any self-mirror like "aa" is still waiting, add 2 for the center.

It never mutates a counter that it is also iterating over, so the original bug cannot occur. And it makes one pass. Faster?

---

### 💥 The Benchmark (best of 5 runs, milliseconds)

| Workload | Count, then Pair | Streaming | Result |
| :--- | :--- | :--- | :--- |
| 100,000 random words, 26 letters | **4.29** | 28.61 | 6.7x slower |
| 100,000 words, sorted | **3.46** | 30.91 | 8.9x slower |
| 1,000,000 random words, 26 letters | **54.06** | 303.73 | 5.6x slower |
| 1,000,000 words, 2 letters (4 distinct) | **47.15** | 274.92 | 5.8x slower |
| 1,000,000 copies of one word | **43.77** | 332.53 | 7.6x slower |

---

### 🔍 Why the Single Pass Lost

1️⃣ **`Counter` counts in C**:
It does the whole pass over $n$ words at C speed. The streaming loop runs Python bytecode for every word: reverse it, look it up, update it.

2️⃣ **The pairing step is tiny**:
There are at most 676 distinct two-letter words, so the pairing loop touches at most 676 items, whatever $n$ is.

3️⃣ **Streaming allocates a reversed string per word**:
One million string reversals add up. The counting version reverses only distinct words.

4️⃣ **Constraints are a gift**:
A small, fixed alphabet makes the second phase essentially constant-time.

---

### 🧪 Verification

Verified with pytest and Hypothesis, 63 passing tests plus 4 expected failures:
- **Brute-Force Oracle**: Both correct versions match an exhaustive search over every ordered selection of words on small inputs.
- **Properties**: Results are always even, shuffling the input changes nothing, and adding a word never shortens the palindrome.
- **100% Agreement**: Both correct versions return identical answers across random workloads.
- **The Original**: Documented with four strict `xfail` tests that reproduce the bug.

---

### 🎯 Key Takeaway

Correctness first: a shuffle test and a brute-force oracle catch order-dependent bugs.
Then speed: "one pass" is not automatically faster than "two passes" when one of them runs in C and the other in Python.

What was the last "obviously faster" rewrite that a benchmark proved wrong? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Greedy #HashMap #Benchmarking #LeetCode #CodingInterview
