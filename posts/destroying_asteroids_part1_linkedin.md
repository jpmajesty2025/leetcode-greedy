# Sort First, Survive Longer: Greedy Asteroid Destruction (Part 1 of 2) 🪐

**The Problem**:
Given a planet's starting `mass` and an array of asteroid masses, you choose the collision order.
If the planet's mass is $\ge$ the asteroid's, the asteroid is destroyed and the planet absorbs its mass. Otherwise, the planet is destroyed. Can the planet destroy every asteroid?

---

### 🧩 Why Brute Force Fails

There are $n!$ possible collision orders.
Checking each one is hopeless for $n$ up to $10^5$.

---

### 🔧 The Greedy Insight

Every asteroid you destroy makes the planet **stronger**.
So always fight the **lightest** remaining asteroid first:

1. Sort the asteroids ascending.
2. Walk through them with a running `mass`.
3. If `mass < asteroid`, return `False`. Otherwise add the asteroid to `mass`.
4. If the loop finishes, return `True`.

---

### 🧠 Why Is Sorted Order Optimal?

An exchange argument:
- Suppose a winning order hits a heavy asteroid before a lighter one.
- Swap them. The lighter one is easier to beat, and the heavier one now meets a planet with at least as much mass as before.
- Every swap keeps the plan valid, so the sorted order never loses a game that any other order wins.

The failure case is just as clean:
- If the sorted order gets stuck at asteroid $a$, every remaining asteroid is $\ge a$.
- No other order can get past them either.

---

### 📊 Complexity

- **Time:** O(n log n) for the sort, then one O(n) pass
- **Space:** O(1) auxiliary with the in-place sort, O(n) with `sorted()`

Edge cases worth checking:
- Equal mass wins (`>=`, not `>`).
- An empty list returns `True`.
- Python integers don't overflow. In Java or C++ the mass needs a `long`.

---

### 🎯 Key Takeaway

When every success makes you stronger, take the cheapest win first.

In Part 2, we will see where a **lazy min-heap** beats the sort, and where it loses badly.

Have you ever been bitten by a function that quietly sorted your input? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Greedy #Sorting #CodeReview #LeetCode #CodingInterview
