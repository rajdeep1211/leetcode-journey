# 176. Second Highest Salary

**Difficulty:** Medium  
**Category:** Database  
**Primary Pattern:** SQL  
**Topics:** Database

---

## 🧩 Problem

See [`question.md`](./question.md) for the complete problem statement.

---

## 💭 My Solving Notes

<!-- AUTO-NOTES-START -->

## Approach

Use DISTINCT to ignore duplicate salaries, sort salaries in descending order, then select the second row with LIMIT 1 OFFSET 1.
A scalar subquery ensures the query always returns one row. If a second distinct salary does not exist, it returns NULL.

## Complexity

- Time: O(n log n) due to sorting the distinct salaries.
- Space: O(n) in the worst case for storing distinct salaries.

## Notes

- DISTINCT is necessary because the question asks for the second highest distinct salary.
- OFFSET 1 skips the highest salary.
- Without the scalar subquery, the result would contain no rows when a second highest salary does not exist, rather than one row with NULL.

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

- Database
