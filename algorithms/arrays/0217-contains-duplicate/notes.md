## Approach

Use a Hash Set to keep track of the elements we have already seen.

Traverse the array:

If the current number is already present in the set, a duplicate exists → return True.
Otherwise, add the number to the set.
If the entire array is traversed without finding a duplicate, return False.
Core Idea
seen = set()

for num in nums:
    if num in seen:
        return True
    seen.add(num)

return False

A set is used because it provides O(1) average-time lookup.

Code
class Solution:
    def containsDuplicate(self, nums):
        seen = set()

        for num in nums:
            if num in seen:
                return True
            seen.add(num)

        return False

## Complexity

Time Complexity
O(n)

Each element is checked and inserted into the set once.

Space Complexity
O(n)

In the worst case, all n elements are unique and stored in the set.

## Notes

This is a classic Hash Set problem.
Use a set when you need to efficiently check whether an element has appeared before.
Duplicate detection can be reduced to:
Have I seen this element before?
        ↓
      Yes → Duplicate
        ↓
       No → Add it
The moment a duplicate is found, return True — no need to traverse the remaining array.
If the loop finishes, every element was unique → return False.
Pattern to Remember

When the problem asks whether something has appeared before, think Hash Set.
