# String Replace vs. Pure Arithmetic: A 25x Surprise (Part 2 of 2) 🧮

In Part 1, we solved Maximum 69 Number with a single `str.replace(..., 1)`.

A common objection: "Converting to a string is cheating. Do it with math."

So I wrote the **Arithmetic** version:
1. Walk the digits from least to most significant with `divmod`.
2. Remember the place value of the most recent 6.
3. The walk ends at the top digit, so the last 6 seen is the **leftmost** one.
4. Add $3 \times$ that place value.

No strings, O(1) extra space. Faster, right?

---

### 💥 The Benchmark (best of 7 runs, per call)

| Input | String Replace | Arithmetic | Result |
| :--- | :--- | :--- | :--- |
| 4 digits (`9669`) | 389 ns | 389 ns | Tie |
| 18 digits | 365 ns | 1,957 ns | **5.4x slower** |
| 1,000 digits | 17,352 ns | 428,551 ns | **25x slower** |
| 1,000 digits, all 6s | 22,996 ns | 507,914 ns | **22x slower** |

---

### 🔍 Why Math Lost

1️⃣ **Big-O hides the constant**:
Both versions are linear in the number of digits. But `replace` is a single C-level scan.
The arithmetic loop runs Python bytecode on every digit.

2️⃣ **Each `divmod` is not O(1) on big integers**:
Dividing a large integer by 10 touches every internal limb, so the loop behaves quadratically for very long numbers. That is why 1,000 digits is so much worse than 18.

3️⃣ **Strings are not always cheating**:
For a problem about *digits*, the decimal representation is the natural data structure.

---

### ⚖️ But the Math Version Has a Hidden Win

Python caps `str()` conversion at **4,300 digits** by default, to guard against denial-of-service from huge inputs.
I tested a 5,000-digit number:
- **String version**: raises `ValueError`.
- **Arithmetic version**: returns the right answer.

So the "slow" version works where the "fast" one crashes. It's irrelevant for LeetCode (at most 4 digits), but relevant for code that handles untrusted input.

---

### 🧪 Verification

Verified with pytest and Hypothesis, 32 passing tests plus 1 expected failure:
- **Brute-Force Oracle**: Both versions match an exhaustive check of every single-digit flip.
- **Properties**: The result is never smaller, keeps the same length, contains only 6s and 9s, and differs in at most one digit.
- **100% Agreement**: Both implementations return identical answers on random inputs.

---

### 🎯 Key Takeaway

Use the string version for speed and clarity.
Reach for arithmetic only when you need to dodge a representation limit.
And never assume that "no extra space" means "faster".

Have you ever "optimized" something away from strings and made it slower? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Benchmarking #Greedy #Performance #LeetCode #CodingInterview
