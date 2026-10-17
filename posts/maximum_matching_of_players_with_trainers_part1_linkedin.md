# Weakest Trainer, Weakest Player: Greedy Two Pointers for Matching Players With Trainers (Part 1 of 2) 🏋️

**The Problem**:
Each player has an ability `players[i]`. Each trainer has a training capacity `trainers[j]`.
A player can match a trainer if ability <= capacity. Each player and each trainer is used **at most once**.

What is the maximum number of matchings?

---

### 🧩 Why Brute Force Fails

Trying every pairing is an assignment problem with factorially many options.
With up to 10^5 players and trainers, that is hopeless. We need structure.

---

### 🔧 The Greedy Strategy

1. Sort players ascending and trainers ascending.
2. Keep two pointers: the weakest unmatched player and the weakest unused trainer.
3. If the trainer can handle the player, count a match and advance both pointers.
4. Otherwise the trainer is too weak for this player, so **skip the trainer**: advance only the trainer pointer.
5. Return the match count.

---

### 🧠 Why Is It Optimal?

An exchange argument:
- If the weakest trainer cannot handle the weakest player, it cannot handle anyone left. Skipping it loses nothing.
- If it can, matching them is never worse. Suppose an optimal plan pairs that player with a stronger trainer. Swap so the weak trainer takes the player, and the stronger trainer is freed for someone else. The count never drops.

The smallest sufficient trainer goes to the weakest player: no capacity is wasted.

---

### 🐛 One Quality Issue

`players.sort()` and `trainers.sort()` reorder **both** of the caller's lists in place.
It passes LeetCode, but a function that returns a count should not quietly rearrange its inputs.

I wrote a strict `xfail` test that documents the mutation and will flag it when it is fixed.
Beyond that, the logic held up. A brute-force oracle over small random inputs found no wrong answers.

---

### 📊 Complexity

- **Time:** O(n log n + m log m) for the sorts, then one linear pass
- **Space:** O(1) auxiliary with in-place sorts (but it mutates the input)

---

### 🎯 Key Takeaway

When matching is "at least as big as", sort both sides and pair the smallest supply that works with the smallest demand.
Sorting turns an assignment problem into two pointers.

In Part 2, I compare it with a non-mutating refactor and a lazy two-heap version.

Which "sort then two pointers" problem taught you the most? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Greedy #TwoPointers #Sorting #LeetCode #CodingInterview
