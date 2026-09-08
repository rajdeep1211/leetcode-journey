# 121. Best Time to Buy and Sell Stock

**Difficulty:** Easy  
**Category:** Algorithms  
**Primary Pattern:** Dynamic Programming  
**Topics:** Array, Dynamic Programming

---

## 🧩 Problem

See [`question.md`](./question.md) for the complete problem statement.

---

## 💭 My Solving Notes

<!-- AUTO-NOTES-START -->

## Approach
Use a Greedy + One Pass approach.

The goal is to find the maximum profit:

profit = sellingPrice - buyingPrice

While traversing the array:

Keep track of the minimum price seen so far.
For the current price, calculate the profit if we sell today.
Update the maximum profit.
Continue for every price.
Core Idea
min_price = min(min_price, price)
max_profit = max(max_profit, price - min_price)

We only need to remember the cheapest price before the current day. This automatically ensures that the stock is bought before it is sold.

Example
prices = [7, 1, 5, 3, 6, 4]

Minimum price → 1
Best selling price → 6

Maximum profit = 6 - 1 = 5
Code
class Solution:
    def maxProfit(self, prices):
        min_price = float('inf')
        max_profit = 0

         for price in prices:
            min_price = min(min_price, price)
            max_profit = max(max_profit, price - min_price)

        return max_profit
## Complexity

Time Complexity
O(n)

The array is traversed only once.

Space Complexity
O(1)

Only two variables are used:

min_price
max_profit

## Notes

This is a classic Greedy / One-Pass problem.
Always maintain the minimum value seen so far.
For every current value, calculate the possible profit using that minimum.
Do not simply find the global minimum and maximum because the minimum must occur before the maximum.
If prices continuously decrease, the answer is 0.
Initialize max_profit = 0 because we are allowed to make no transaction.
The key pattern is:
Minimum So Far
      ↓
Current Value
      ↓
Current Profit
      ↓
Maximum Profit
Pattern to Remember

When looking for the maximum difference where the smaller value must come before the larger value, think "minimum so far + maximum difference."

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
- Dynamic Programming
