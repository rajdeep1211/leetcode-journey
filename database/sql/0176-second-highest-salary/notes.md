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
