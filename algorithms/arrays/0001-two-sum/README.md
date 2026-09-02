# 1. Two Sum

**Difficulty:** Easy  
**Category:** Algorithms  
**Primary Pattern:** Hash Table  
**Topics:** Array, Hash Table

---

## 🧩 Problem

See [`question.md`](./question.md) for the complete problem statement.

---

## 💭 My Solving Notes

<!-- AUTO-NOTES-START -->

## Approach

### Initial Thought

My first thought was to check every possible pair of numbers and see if their sum equals the target.

### Observation

The brute-force approach would take O(n²). Instead of repeatedly searching for the required number, I can store numbers that I have already seen in a hash map.

### Final Approach

For each number, I calculate:

target - current number

If that value is already present in the hash map, I have found the required pair.

Otherwise, I store the current number and its index in the hash map.

---

## Complexity

**Time:** `O(n)`

**Space:** `O(n)`

---

## Notes

- Hash maps provide fast average O(1) lookup.
- The complement technique is useful for pair-sum problems.
- Always consider whether previously processed values can be stored for faster lookup.

<!-- AUTO-NOTES-END -->

---

## 💻 Solution

The accepted C++ solution is available in [`solution.cpp`](./solution.cpp).

---

## 🧠 Key Takeaway

The complement technique combined with a hash map can reduce a pair-search problem from O(n²) to O(n).

---

## 🔗 Related Topics

- Array
- Hash Table
