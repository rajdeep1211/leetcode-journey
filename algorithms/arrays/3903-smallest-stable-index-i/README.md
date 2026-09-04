# 3903. Smallest Stable Index I

**Difficulty:** Easy  
**Category:** Algorithms  
**Primary Pattern:** Array  
**Topics:** Array, Prefix Sum

---

## 🧩 Problem

See [`question.md`](./question.md) for the complete problem statement.

---

## 💭 My Solving Notes

<!-- AUTO-NOTES-START -->

## Approach
For each index i, the instability score is:
max(nums[0..i]) - min(nums[i..n-1])
We need to find the first index where this score is less than or equal to k.
To do this efficiently:
1. Precompute suffixMin[i], which stores the minimum value from index i to the end of the array.
2. Traverse the array from left to right while maintaining prefixMax, the maximum value seen so far.
3. At every index i:
   - prefixMax gives max(nums[0..i])
   - suffixMin[i] gives min(nums[i..n-1])
4. If:
   prefixMax - suffixMin[i] <= k
   then i is stable. Return it immediately because we are checking indices from left to right.
   
## Complexity
Time Complexity: O(n)
- One right-to-left traversal to build suffixMin
- One left-to-right traversal to find the first stable index

Space Complexity: O(n)
- For the suffixMin array
  
## Notes
- prefixMax is maintained using a single variable, so no separate prefix array is needed.
- The first stable index found is the smallest stable index.
- Use long when subtracting to safely handle large values:
  
(long) prefixMax - suffixMin[i]

<!-- AUTO-NOTES-END -->

---

## 🔎 Algorithm

The algorithm is documented in the solving notes above.

---

## ⏱️ Complexity

See the complexity section in `notes.md`.

---

## 💻 Solution

The accepted solution is available in the solution file.

---

## 🧠 Key Takeaway

See the key learning in `notes.md`.

---

## 🔗 Related Topics

- Array
- Prefix Sum
