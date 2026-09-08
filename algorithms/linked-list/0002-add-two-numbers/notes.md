## Approach

Use a Linked List Traversal + Carry approach.

The two numbers are represented in reverse order, meaning the first node contains the least significant digit.

Traverse both linked lists simultaneously and add their digits along with a carry.

Steps
Create a dummy node to simplify result-list construction.
Keep a pointer current to build the result.
While either list still has nodes or there is a remaining carry:
Get the current digit from each list.
Add both digits and the carry.
Store the last digit using % 10.
Update the carry using // 10.
Create a new node for the result.
Return dummy.next.
Core Formula
sum = digit1 + digit2 + carry

digit = sum % 10
carry = sum // 10
Example
l1 = 2 → 4 → 3
l2 = 5 → 6 → 4

  342
+ 465
-----
  807

Because the lists store digits in reverse order:

2 + 5 = 7
4 + 6 = 10 → digit = 0, carry = 1
3 + 4 + 1 = 8

Result:

7 → 0 → 8
Code
class Solution:
    def addTwoNumbers(self, l1, l2):
        dummy = ListNode(0)
        current = dummy
        carry = 0

        while l1 or l2 or carry:
            digit1 = l1.val if l1 else 0
            digit2 = l2.val if l2 else 0

            total = digit1 + digit2 + carry

            carry = total // 10
            digit = total % 10

            current.next = ListNode(digit)
            current = current.next

            if l1:
                l1 = l1.next

            if l2:
                l2 = l2.next

        return dummy.next

## Complexity

Time Complexity
O(max(m, n))

Where m and n are the lengths of the two linked lists.

Each node is visited at most once.

Space Complexity
O(max(m, n))

The result linked list requires at most max(m, n) + 1 nodes because of a possible final carry.

## Notes

This is a classic Linked List + Carry problem.
The digits are stored in reverse order, so addition can be performed from left to right through the lists.
Always include the carry when calculating the next digit.
The lists may have different lengths, so treat a missing node as 0.
The loop must continue if there is a remaining carry:
while l1 or l2 or carry:
The % 10 gives the digit that belongs in the current node.
The // 10 gives the carry for the next position.
A dummy node makes result-list construction easier and avoids special handling for the first node.
No need to convert the linked lists into integers; direct traversal is simpler and avoids issues with very large numbers.
Pattern to Remember

When adding numbers represented by linked lists, think: digit + digit + carry → new digit + carry.
