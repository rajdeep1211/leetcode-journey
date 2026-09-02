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
