# Bitmask vs Last-Seen Index: Two Ways to Track the Current Piece (Part 2 of 2) 🧮

In Part 1, the set-based greedy for **Optimal Partition of a String** was correct once I removed a stray `self` parameter. Both alternatives here keep the same greedy and change only how we remember the current substring.

---

### ✅ Alternative 1: Bitmask

Lowercase letters fit in 26 bits, so one integer can be the "set".
- Bit 0 means 'a', bit 25 means 'z'.
- If the letter's bit is already set, count a new piece and reset the mask to 0.
- Then set the bit.

No set object, no hashing, and "clear" is just assigning 0.

**Time:** O(n)
**Space:** O(1)

The tradeoff: it depends on the lowercase guarantee. I made it raise `ValueError` on anything else instead of quietly computing a nonsense bit.

---

### ✅ Alternative 2: Last-Seen Index

Instead of clearing anything, remember where each letter last appeared and where the current piece started.
- A repeat exists exactly when a letter's last index is at or after the piece start.
- When that happens, start a new piece at the current index.
- Old entries are never deleted. They fall before the start and are ignored.

This avoids the "reset" step completely, and it works for any characters, not just lowercase letters.

**Time:** O(n)
**Space:** O(min(n, alphabet size))

---

### 🧪 How I Tested It

- Both LeetCode examples, plus a singleton, the empty string, the full alphabet, and a repeat only at the very end.
- A brute force that tries all 2^(n-1) ways of cutting the string, for small random inputs.
- A reconstruction test: rebuild the pieces, check they join back into the original string, and check each piece is all-unique.
- The bound `ceil(n / 26) <= answer <= n`, and monotonicity: extending the string never lowers the count, and a prefix never needs more.
- A regression test that calls each function with a single string argument, the call that failed before.
- Bitmask rejects uppercase, digits, spaces and accents. Last-seen accepts them.
- 100,000-character inputs at both extremes.

All three agree everywhere.

---

### 🎯 Key Takeaways

1. The greedy decision stays the same. Only the bookkeeping changes.
2. A bitmask is a natural fit when the alphabet is small and fixed, but it needs validation.
3. "Never clear, just compare against a start index" is a general trick for sliding windows.
4. Test the way callers use your code, not just the logic inside it.

Which would you pick in an interview, the set, the bitmask, or the last-seen index? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Greedy #Strings #BitManipulation #Testing #Hypothesis #LeetCode #CodingInterview
