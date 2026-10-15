# Load the Densest Boxes First: Greedy Fractional Knapsack in Disguise (Part 1 of 2) 🚚

**The Problem**:
You have box types `[numberOfBoxes, unitsPerBox]` and a truck that holds at most `truckSize` boxes.

What is the maximum total number of units you can load?

---

### 🧩 Every Box Costs the Same

Each box takes exactly **one slot**, no matter how many units it holds.
So the only question is: which `truckSize` boxes carry the most units?

That is the easy cousin of the knapsack problem. With unit weights, greedy is exactly optimal.

---

### 🔧 The Greedy Strategy

1. Sort box types by `unitsPerBox` in **descending** order.
2. For each type, take `min(numberOfBoxes, remaining capacity)` boxes.
3. Add `boxes_taken * unitsPerBox` to the total and shrink the remaining capacity.
4. Stop when the truck is full.

---

### 🧠 Why Is It Optimal?

An exchange argument:
- Suppose an optimal load skips a box with $u_1$ units but includes a box with $u_2 < u_1$ units.
- Swap them. The truck still holds the same number of boxes, and the total changes by $u_1 - u_2 > 0$.
- So a load that skips a denser box for a lighter one is never better.

Repeating the swap turns any optimal load into the greedy one.

---

### 🐛 Quality Notes on My First Draft

1. **`boxTypes.sort()` mutates the caller's list.** It passes LeetCode but reorders data the function doesn't own. `sorted()` fixes it.
2. **`camelCase` parameters in Python.** They match LeetCode's signature, so I kept them. Elsewhere `box_types` and `truck_size` would be idiomatic.
3. **Reassigning the `truckSize` parameter** works, but a separate `remaining` variable reads more clearly.

The mutation issue is captured in a test marked `xfail(strict=True)`.

---

### 📊 Complexity

- **Time:** O(n log n) for the sort, then one O(n) pass
- **Space:** O(1) auxiliary with the in-place sort

---

### 🎯 Key Takeaway

When every item has the same cost, "best value first" is provably optimal.
Spotting a knapsack with **uniform weights** turns a hard problem into a sort.

In Part 2, we will drop the sort entirely, using a **bucket** approach, and see exactly when that wins.

Where have you spotted an easy problem hiding inside a famous hard one? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Greedy #Sorting #Knapsack #LeetCode #CodingInterview
