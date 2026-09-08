# 175. Combine Two Tables

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

Use a LEFT JOIN to combine the Person table with the Address table.

The goal is to return every person along with their address information if an address exists.

Join the tables using the common column:

Person.personId = Address.personId

A LEFT JOIN is important because we must keep all records from Person, even when a person does not have an entry in Address.

Core Idea
SELECT
    p.firstName,
    p.lastName,
    a.city,
    a.state
FROM Person p
LEFT JOIN Address a
    ON p.personId = a.personId;

## Complexity

Time Complexity
O(P + A)

Approximately linear in the number of rows when the join columns are appropriately indexed.

Space Complexity
O(P + A)

Depending on the database engine and execution strategy, the join may require additional memory for intermediate/join structures.

## Notes

This is a basic SQL JOIN problem.
Use LEFT JOIN when all rows from the left table must be preserved.
Person is the left table because every person must appear in the result.
If no matching address exists, city and state will be NULL.
The relationship is established using:
Person.personId = Address.personId
JOIN Pattern to Remember
LEFT TABLE
   ↓
LEFT JOIN
   ↓
RIGHT TABLE
   ↓
ON matching_condition
Key Difference
INNER JOIN → only matching records
LEFT JOIN  → all left records + matching right records

If the question says "include all records from table A, even if there is no match in table B", think LEFT JOIN.

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
