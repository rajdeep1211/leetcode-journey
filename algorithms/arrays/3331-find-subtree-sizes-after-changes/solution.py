// 605 ms | 52.1 MB
class Solution:
    def findSubtreeSizes(self, parent: List[int], s: str) -> List[int]:
        from typing import List

class Solution:
    def findSubtreeSizes(self, parent: List[int], s: str) -> List[int]:
        n = len(parent)
        children = [[] for _ in range(n)]
        for i in range(1, n):
            children[parent[i]].append(i)

        new_parent = parent[:]
        last = [-1] * 26
        order = []  # preorder of the original tree

        # iterative DFS: (node, state) state 0 = enter, 1 = exit
        # saved[node] holds the previous last[c] to restore on exit
        saved = [-1] * n
        stack = [(0, 0)]
        while stack:
            x, state = stack.pop()
            c = ord(s[x]) - 97
            if state == 0:
                order.append(x)
                if x != 0 and last[c] != -1:
                    new_parent[x] = last[c]
                saved[x] = last[c]
                last[c] = x
                stack.append((x, 1))
                for ch in children[x]:
                    stack.append((ch, 0))
            else:
                last[c] = saved[x]

        size = [1] * n
        for x in reversed(order):
            if x != 0:
                size[new_parent[x]] += size[x]
        return size