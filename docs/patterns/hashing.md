# Hashing

## 🧠 What Is Hashing?

Hashing is a technique used to store and retrieve information efficiently using a hash-based data structure such as a hash map or hash set.

The main advantage is fast average-case lookup, insertion, and deletion.

Typical operations are:

- Lookup → `O(1)` average
- Insert → `O(1)` average
- Delete → `O(1)` average

---

## 🔍 When Should I Think About Hashing?

Consider hashing when the problem involves:

- Fast lookup
- Checking whether something already exists
- Counting frequencies
- Finding duplicates
- Finding complements
- Mapping one value to another
- Tracking previously processed elements

A useful question to ask is:

> "Do I need to remember something I have already seen?"

If yes, a hash map or hash set may be useful.

---

## 🛠️ Common Techniques

### 1. Hash Set

Use a set when you mainly need to know:

> "Have I seen this value before?"

Example:

```text
nums = [1, 2, 3, 1]

seen = {}

1 → add
2 → add
3 → add
1 → already exists
