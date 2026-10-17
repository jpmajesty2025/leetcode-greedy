# Flip the Most Negative First, Then Let Parity Decide (Part 1 of 2) ➖

**The Problem**:
You must negate exactly `k` elements of an array. You choose the index each time, and you may pick the same index more than once.

What is the largest possible sum afterward?

---

### 🧩 Two Regimes

**While negatives remain**, each flip should turn the most negative number positive.
That gains $2|x|$ per flip, so go in ascending order and stop after $k$ flips.

**Once everything is non-negative**, every extra flip costs something:
- Flipping the same element twice cancels, so extra flips come in useless pairs.
- Only the **parity** of the leftover flips matters.
- If an odd one is left, spend it on the element with the **smallest absolute value**, which loses $2 \cdot \min |x|$.
- If a zero is present, that costs nothing.

---

### 🔧 The Algorithm

1. Sort a **copy** of the array ascending.
2. Walk it, negating each negative number while flips remain.
3. If flips remain and $k$ is odd, subtract twice the smallest absolute value.
4. Return the sum.

---

### 🧠 Why Is It Optimal?

An exchange argument:
- Flipping a negative number is always a gain, and a more negative number gains more. So the flips go to the most negative numbers first.
- After the negatives are gone, any flip loses value. The loss is smallest on the smallest absolute value, and pairs of flips on the same element cancel entirely.

My brute-force oracle, which tries every sequence of $k$ index choices, agrees on every small input.

---

### 🛠️ Three Design Choices

1. **Sort a copy, not the input.** Sorting the caller's list in place reorders it, and flipping values inside it changes the data the caller still holds. A function that returns a number should leave its arguments alone.
2. **Use `min()` for the leftover flip.** After the loop, one O(n) pass finds the smallest absolute value. A second full sort would cost O(n log n) for the same answer.
3. **Name it for what it does.** Typos in a function name, like a stray capital letter in the middle, make code harder to search and trust.

A test asserts that the input list is unchanged afterward.

---

### 📊 Complexity

- **Time:** O(n log n) for the sort, then one O(n) pass
- **Space:** O(n) for the sorted copy

---

### 🎯 Key Takeaway

For "exactly $k$" operations that can undo themselves, think in terms of **parity**.
Pairs of flips vanish, so after the real gains are taken, only one bit of information is left.

In Part 2, I compare this sort-based solution with a heap and a counting version. The heap wins in some cases and loses badly in others.

What is your favorite problem where parity did the heavy lifting? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Greedy #Sorting #CleanCode #LeetCode #CodingInterview
