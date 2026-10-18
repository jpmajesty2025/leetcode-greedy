# Pairs Outside, Biggest Leftover in the Middle: Largest Palindromic Number (Part 1 of 2) 🔢

**The Problem**:
Given a string of digits, build the **largest palindromic integer** using any subset of those digits, reordered as you like. It must have no leading zeros, and you must use at least one digit.

---

### 🧩 Why Brute Force Fails

Choosing a subset and arranging it gives factorially many candidates, and each one still needs a palindrome check.
The input can be 10^5 digits long. We need structure.

---

### 🔧 The Greedy Strategy

1. Count each digit.
2. Go from 9 down to 0. A digit with count `c` contributes `c // 2` copies to the **left half**.
3. The largest digit with a leftover (odd count) becomes the **centre**.
4. Mirror the left half to get the right half.

---

### 🧠 Why Is It Optimal?

- **Longer wins.** A longer number is larger, so use as many pairs as possible, then add a centre if one is left.
- **Bigger digits first.** The left half decides the comparison, so fill it with the biggest available pairs first.
- **Centre choice.** One leftover digit fits in the middle. The largest candidate gives the largest number.

---

### 🐛 The Bug: Leading-Zero Handling

The original raised `ValueError` whenever the result started with '0'. That fails valid inputs:

- `"0000"` should return `"0"`, but it raised.
- `"0"` should return `"0"`, but it raised.
- `"00009"` should return `"9"`, but it raised.
- `"0001"` should return `"1"`, but it raised.

The cause: with only zeros paired, the half is all zeros, so the whole palindrome is padded with leading zeros. But the right answer is not an error. It is the centre digit alone, or just `"0"` if nothing else exists.

The fix is to drop an all-zero half. Zeros that sit **between** bigger pairs, like `"0011"` giving `"1001"`, stay.

Smaller cleanups:
- The docstring claimed "only zeros" is an error. It is a valid answer.
- `import Counter` moved from inside the function to the top of the file.
- Non-digit input now raises a clear `ValueError` instead of producing nonsense.

---

### 📊 Complexity

- **Time:** O(n) to count, plus a sort of at most 10 distinct digits
- **Space:** O(n) for the output

---

### 🎯 Key Takeaway

When a validity rule rejects a result, ask whether the right response is an error or a smaller valid answer. Here the "invalid" case was just a padding problem.

In Part 2, I compare a fixed counting array and a sorted pairing scan.

Where has an "edge case" turned out to be a normal case for you? Tell me below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Greedy #Strings #Palindrome #LeetCode #CodingInterview
