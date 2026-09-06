# 181. Employees Earning More Than Their Managers

**Difficulty:** Easy  
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
Self-join the Employee table:
- e represents an employee.
- m represents that employee’s manager.
- Match them using e.managerId = m.id.
- Return employees whose salary is greater than their manager’s salary.
Complexity

## Complexity
- Time: O(n) with an index on id.
- Space: O(1) auxiliary space, excluding the result table.
  
## Notes
- Employees with managerId = NULL are naturally excluded by the JOIN.
- AS Employee gives the output column the required name.

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
