// 254 ms | 19.8 MB
from collections import Counter
from typing import List

class Solution:
    def largestOverlap(self, img1: List[List[int]], img2: List[List[int]]) -> int:
        ones1 = []
        ones2 = []

        for r in range(len(img1)):
            for c in range(len(img1)):
                if img1[r][c] == 1:
                    ones1.append((r, c))
                if img2[r][c] == 1:
                    ones2.append((r, c))

        shifts = Counter()

        for r1, c1 in ones1:
            for r2, c2 in ones2:
                # Translation that moves img1's (r1, c1) onto img2's (r2, c2)
                shifts[(r2 - r1, c2 - c1)] += 1

        return max(shifts.values(), default=0)