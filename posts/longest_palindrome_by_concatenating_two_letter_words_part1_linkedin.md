# Pair the Mirrors, Then Pick One Center: A Bug That Passes the Examples (Part 1 of 2) 🪞

**The Problem**:
You are given words made of exactly two lowercase letters.
Pick some of them (each at most once) and concatenate them in any order to build the longest palindrome. What is its length?

---

### 🧩 What Can Go Into a Palindrome?

Two kinds of words matter:
- **Mirror pairs**: "ab" and "ba". Put "ab" on the left and "ba" on the right.
- **Self-mirrors**: "aa", "gg". Two copies pair up with each other. One leftover copy can be the **center**.

A word like "ab" with no "ba" anywhere is useless. And only **one** word can ever be the center.

---

### 🔧 The Counting Strategy

1. Count how many times each word appears.
2. For a self-mirror word with count $f$: add $4 \cdot \lfloor f/2 \rfloor$ letters. If $f$ is odd, a center is available.
3. For "ab" and "ba": add $4 \cdot \min(\text{count}_{ab}, \text{count}_{ba})$ letters. Each pair is counted **once**.
4. If any center is available, add 2.

---

### 🐛 My First Draft Had a Real Bug

To avoid counting "ab" and "ba" twice, the code subtracts the matched pairs from the **partner's** count, but never from the word's own count.

That works only if the word with the larger count is seen first. If the smaller one comes first, the leftover partners get matched a second time.

Example: `["ba", "ab", "ab", "ab"]`
- True answer: 4 (just "abba").
- My first draft returned **8**.

It passed all three LeetCode examples.

---

### 📏 How Often Does It Fail?

I compared it against a corrected version on random inputs:
- 6 words from 3 letters: wrong **10%** of the time
- 20 words from 3 letters: wrong **50%** of the time
- 100 words from 10 letters: wrong **96%** of the time
- 1,000 words from 26 letters: wrong **100%** of the time (2,000 of 2,000 trials)

The bug gets worse with larger inputs. I can't tell whether LeetCode's own tests would catch it, so the lesson is not to rely on the judge.

---

### 🔧 The Fix

Handle each unordered pair once, for example only when `word < reversed(word)`, and read the partner's count without modifying anything.
Mutating a counter while iterating over it makes the answer depend on iteration order. Order-independence is a property worth testing.

---

### 📊 Complexity

- **Time:** O(n)
- **Space:** O(d) where $d \le 676$ distinct words

---

### 🎯 Key Takeaway

If a solution mutates its own data structure while using it, ask what happens under a different iteration order.
A shuffle test and a brute-force oracle would have found this in seconds.

In Part 2, I compare the fix against a single-pass streaming matcher.

Have you ever shipped a bug that only appeared for larger inputs? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Greedy #HashMap #Testing #LeetCode #CodingInterview
