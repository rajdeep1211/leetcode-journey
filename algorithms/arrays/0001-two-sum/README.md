# 1. Two Sum

**Difficulty:** Easy  
**Category:** Algorithms  
**Primary Pattern:** arrays  
**Topics:** Array, Hash Table

---

## Problem

See [`question.md`](./question.md) for the complete problem statement.

---

## Approach

### Thought Process

Write your reasoning here.

- What was your first idea?
- What observation helped?
- Why does the final approach work?

### Algorithm

1. Identify the key observation.
2. Apply the chosen data structure or algorithm.
3. Process the input.
4. Return the result.

---

## Complexity

**Time:** `O(?)`

**Space:** `O(?)`

---

## Solution

The accepted LeetCode solution is available in the solution file.

---

## My Notes

## Approach

## Complexity

## Notes

---

## Key Takeaway

Write the main concept or pattern learned from this problem.

---

## Related Topics

- Array, - Hash Table

<!-- AUTO-NOTES-START -->

## 💭 My Solving Notes

# My Solving Notes

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
