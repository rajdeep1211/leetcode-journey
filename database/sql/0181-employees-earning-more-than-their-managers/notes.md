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
