# Work Backwards: Halve When You Can, Subtract When You Must (Minimum Moves to Reach Target Score, Part 1 of 2) 🎯

**The Problem**:
Start at 1 and reach `target`. Each move either adds 1 or doubles the number, and you may double at most `maxDoubles` times. Return the minimum number of moves.

---

### 🧩 Why Forward Search Struggles

Going forward, every number has two options, so the search tree doubles at each level. A breadth-first search over (value, doubles used) works for small targets, but `target` goes up to 10^9.

Going **backward** removes the choice.

---

### 🔧 The Greedy Strategy (Reverse the Game)

Start at `target` and walk down to 1:
1. If the number is even and you still have doubles, **halve** it.
2. Otherwise, **subtract 1**.
3. Count every step.

Reversing the moves turns "add 1" into "subtract 1" and "double" into "halve".

---

### 🧠 Why Is It Optimal?

- **Halving shrinks the number far more than subtracting.** A single halving is worth about half the remaining distance, so every available double should be used.
- **Doubles are most valuable late.** Going forward, a double near the end multiplies a larger number. Going backward, that means halving first, from the big end.
- **Odd numbers must be fixed first.** You can only halve an even number, so an odd one needs one subtraction before it can be halved.

I also checked this against a forward breadth-first search on random targets up to 80 with up to 8 doubles. The two agreed every time.

---

### 🐢 The Hidden Performance Trap

The original is correct. But once the doubles run out, it subtracts 1 per loop iteration.

With `maxDoubles = 0` and `target = 10^9`, that is a billion iterations. I measured 0.66 seconds for 10^7, so the full limit would take over a minute in Python.

The fix is one line: when no doubles remain, add `target - 1` to the count and stop. Now the loop runs at most about 2 log(target) times.

Other cleanups:
- A target below 1 returned 0 without any error. That value is unreachable from 1, so it now raises `ValueError`.
- A negative `maxDoubles` is rejected too.

---

### 📊 Complexity

- **Time:** O(log target) after the fix
- **Space:** O(1)

---

### 🎯 Key Takeaway

Correct and fast are different checks. A greedy that is optimal in its choices can still hide a loop that runs linearly in the value. Always ask what happens when one of the resources is zero.

In Part 2, I show a bit-counting formula with no loop at all.

Have you ever found a linear loop hiding in a "logarithmic" solution? Tell me below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Greedy #Math #Performance #LeetCode #CodingInterview
