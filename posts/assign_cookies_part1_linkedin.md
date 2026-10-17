# Smallest Cookie That Works: The Two-Pointer Greedy Behind Assign Cookies (Part 1 of 2) 🍪

**The Problem**:
Each child has a greed factor `g[i]`: the minimum cookie size that will make them content.
Each cookie has a size `s[j]`, and each child gets **at most one** cookie.

What is the maximum number of content children?

---

### 🧩 Why Brute Force Fails

Matching children to cookies is an assignment problem with $n!$ possible pairings.
We need structure to cut it down.

---

### 🔧 The Greedy Strategy

1. Sort the greed factors and cookie sizes ascending.
2. Keep two pointers: the least greedy child still waiting, and the smallest unused cookie.
3. If the cookie is big enough, the child is content: advance both pointers.
4. If it is too small, **discard the cookie**: advance only the cookie pointer.
5. Return the number of content children.

---

### 🧠 Why Is It Optimal?

An exchange argument:
- The smallest cookie either satisfies the least greedy child, or it satisfies nobody (every other child is at least as greedy).
- If it fits that child, giving it to them is never worse. Any optimal plan that uses a bigger cookie for that child can swap, freeing the bigger cookie for someone else.
- If it doesn't fit, it is useless to everyone, so discarding it loses nothing.

Smallest fitting cookie to the least demanding child: nothing is wasted.

---

### 🐛 One Quality Issue

`g.sort()` and `s.sort()` reorder **both** of the caller's lists in place.
It passes LeetCode, but a function that returns a count should not silently rearrange the data it was given.

The fix is `sorted(g)` and `sorted(s)`, at the cost of O(n + m) extra memory.
A strict `xfail` test documents the mutation and will tell me when I fix it.

Everything else was correct. My brute-force oracle found no wrong answers.

---

### 📊 Complexity

- **Time:** O(n log n + m log m) for the sorts, then a single linear pass
- **Space:** O(1) auxiliary with the in-place sorts

---

### 🎯 Key Takeaway

When one side has a threshold ("at least this big") and you want the most matches, serve the pickiest demand with the smallest supply that works.
Sorting turns an assignment problem into two pointers.

In Part 2, I compare it against a non-mutating refactor and a lazy two-heap version. The heap wins in exactly one scenario.

What is your favorite "sort then two pointers" problem? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #Greedy #TwoPointers #Sorting #LeetCode #CodingInterview
