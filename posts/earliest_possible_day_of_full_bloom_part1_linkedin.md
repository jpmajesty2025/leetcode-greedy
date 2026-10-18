# Plant the Slowest Growers First: Earliest Possible Day of Full Bloom (Part 1 of 2) 🌱

**The Problem**:
You have `n` seeds. Each seed needs `plantTime[i]` days of your work to plant, then `growTime[i]` days to grow on its own before it blooms. You can only work on one seed per day, and you choose the order. Return the earliest day when **every** seed has bloomed.

---

### 🧩 Why Brute Force Fails

Trying every order of planting is n! possibilities. For n up to 10^5 that is not even close. The problem also lets you split a seed's planting across several days, which makes the search space look even bigger.

---

### 🔧 The Greedy Strategy

1. Sort the seeds by **grow time, largest first**.
2. Plant them in that order, adding each seed's planting days to a running total.
3. After planting a seed, its bloom day is the running total plus its grow time.
4. The answer is the largest bloom day over all seeds.

---

### 🧠 Why Is It Optimal?

Think about what you can overlap:
- **Planting is a bottleneck.** You work on one seed at a time, so total planting time is fixed. Nothing changes that.
- **Growing is free.** Seeds grow in parallel while you plant others. The only question is which growth periods hide behind other seeds' planting.
- **Exchange argument.** Take two neighbouring seeds where the earlier one grows faster. Swap them. The pair still finishes planting at the same day, but now the slower grower starts its growth earlier. So the pair's latest bloom day can only stay the same or drop.
- **Interleaving does not help.** Splitting a seed's planting across days only delays when it starts growing, so finishing one seed before starting the next is always at least as good.

Sorting by grow time descending is therefore optimal. Plant time does not matter for the order.

---

### 📊 Complexity

- **Time:** O(n log n)
- **Space:** O(n)

---

### 🎯 Key Takeaway

When one resource is serial (your hands) and another is parallel (growth), schedule the longest parallel work first so it overlaps as much of the serial work as possible.

In Part 2, I look at two ways to avoid sorting every seed.

Where have you seen "start the longest wait first" in real work? Tell me below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Greedy #Scheduling #LeetCode #CodingInterview
