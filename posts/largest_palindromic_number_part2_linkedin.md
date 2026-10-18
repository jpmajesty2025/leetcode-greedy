# Counting Array vs Sorted Pairing: Two More Ways to Build the Palindrome (Part 2 of 2) 🧮

In Part 1, the greedy for **Largest Palindromic Number** was right in spirit, but it raised errors on inputs like "0000" and "00009", where the correct answers are "0" and "9". Here are two alternatives that carry the same fix.

---

### ✅ Alternative 1: Fixed-Size Counting Array

Digits are only 0 to 9, so a list of ten counters replaces both the `Counter` and the sort.
- Count each digit into the list.
- Walk from 9 down to 0, adding `count // 2` copies to the left half.
- The first digit with an odd count becomes the centre.
- If we reach 0 with an empty half, return the centre, or "0" if there is none.

**Time:** O(n)
**Space:** O(1) auxiliary, plus the output

My first draft had a subtle bug here. I tested "is the half empty" by checking an empty list, but I had appended empty strings for digits with no pairs, so the list was never empty. The fix was to append only when a digit actually has a pair. A good reminder that "empty" depends on what you store.

---

### ✅ Alternative 2: Sorted Pairing Scan

Sort the digits descending, so equal digits sit side by side.
- If two neighbours are equal, they form a pair. Consume both.
- Otherwise the lone digit is a centre candidate. The first one seen is the largest.
- Pairs come out already in descending order, which is the best left half.
- Same leading-zero rule: if the first pair is zero, return the centre or "0".

It is the same greedy seen through adjacency instead of counting. The price is the O(n log n) sort.

**Time:** O(n log n)
**Space:** O(n)

---

### 🧪 How I Tested It

- Both LeetCode examples, plus "0", "00", "0000", "0001", "00011", and zeros between bigger pairs.
- A brute force that tries every ordered selection of digits on tiny inputs, keeps the palindromes without leading zeros, and takes the numerically largest.
- Property checks on random inputs up to 200 digits:
  - The result is a palindrome.
  - It has no leading zeros, unless it is "0".
  - It only uses digits that are actually available.
  - All three implementations agree.
- Shuffling the input never changes the answer, and adding a digit never shrinks it.
- Invalid input, such as empty strings, letters, spaces and non-ASCII digits, raises `ValueError`.
- 100,000-digit inputs.

---

### 🎯 Key Takeaways

1. Fix the logic once, then check every alternative against the same cases. The same bug can sneak back in a new shape.
2. With a tiny fixed alphabet, an array of counters beats sorting.
3. A brute-force oracle found nothing wrong after the fix, which is the real evidence the fix is complete.
4. Numerical comparison of strings means comparing length first, then the digits.

Which of the three would you write in an interview? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Greedy #Strings #Palindrome #Testing #Hypothesis #LeetCode #CodingInterview
