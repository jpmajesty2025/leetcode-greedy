# Group or Bucket: Two Ways to Avoid Sorting Every Seed (Part 2 of 2) 🪴

In Part 1, the sorted greedy for **Earliest Possible Day of Full Bloom** was already correct and optimal. These alternatives change how we sort, not what we decide.

---

### ✅ Alternative 1: Group Seeds by Grow Time

Seeds with the same grow time are interchangeable. Only the **last** one planted in the group matters, and by then you have spent the whole group's planting time.

So collapse each group into one entry: the total planting days of its seeds, and the shared grow time.
- Build a dictionary from grow time to total planting days.
- Sort only the **distinct** grow times, largest first.
- Walk them, adding each group's planting days, and track the largest `running total + grow time`.

It is the same answer as sorting every seed. It sorts k distinct values instead of n seeds, which helps when many seeds share a grow time.

**Time:** O(n + k log k)
**Space:** O(k)

---

### ✅ Alternative 2: Bucket by Grow Time

If grow times are small and bounded, skip comparison sorting altogether.
- Make one bucket per possible grow time, from 0 to the maximum.
- Add each seed's planting days to its bucket.
- Sweep the buckets from the largest grow time down to 0, tracking the running total and the best bloom day.

On LeetCode, grow times are at most 10^4, so this is effectively linear.

**Time:** O(n + max grow time)
**Space:** O(max grow time)

The tradeoff is memory. For huge grow times, use the grouped version.

---

### 🧪 How I Tested It

- All three LeetCode examples, plus zero times, planting only, growing only, equal grow times, and a slow grower that must go before a quick planter.
- An exhaustive search of **every order** of planting, on random inputs of up to 6 seeds. All three matched it.
- A second oracle that tries **every day-by-day schedule**, including splitting a seed's planting across days, on up to 3 small seeds. Nothing beat the greedy, which backs up the claim that interleaving does not help.
- Random inputs of up to 200 seeds: all three agree, and the result stays within simple lower and upper bounds.
- Shuffling the seeds never changes the answer, and slower planting or growing never speeds things up.
- Negative values, mismatched lengths and empty lists raise `ValueError`. Inputs are not modified.

---

### 🎯 Key Takeaways

1. If many items share a sort key, sort the distinct keys and carry totals instead.
2. Bucketing beats comparison sorting when the key range is small and bounded.
3. An oracle that is more general than your assumption, like day-by-day scheduling, tests the assumption itself.
4. State the tradeoff: speed for memory, bounded for unbounded.

Which would you reach for first: sort, group or bucket? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Greedy #Scheduling #Sorting #Testing #Hypothesis #LeetCode #CodingInterview
