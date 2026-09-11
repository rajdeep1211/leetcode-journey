// 15 ms | 19.3 MB
class Solution:
    def totalNumbers(self, digits: List[int]) -> int:
        numbers = set()

        for i in range(len(digits)):
            for j in range(len(digits)):
                for k in range(len(digits)):
                    if i == j or j == k or i == k:
                        continue

                    if digits[i] == 0:       # no leading zero
                        continue
                    if digits[k] % 2 != 0:   # must be even
                        continue

                    numbers.add(digits[i] * 100 + digits[j] * 10 + digits[k])

        return len(numbers)