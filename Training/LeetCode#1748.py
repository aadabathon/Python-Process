class Solution(object):
    def sumOfUnique(self, nums):
        unique = []
        sum = 0
        for i in nums:
            if i not in unique:
                unique.append(i)
            else:
                if i*(-1) in unique:
                    pass
                else:
                    unique.append(-1*i)
        for i in unique:
            sum += i
        return sum


# class Solution(object):
#     def sumOfUnique(self, nums):
#         counts = {}

#         for num in nums:
#             if num not in counts:
#                 counts[num] = 1
#             else:
#                 counts[num] += 1

#         total = 0

#         for num in counts:
#             if counts[num] == 1:
#                 total += num

#         return total


# class Solution(object):
#     def sumOfUnique(self, nums):
#         counts = {}

#         for num in nums:
#             counts[num] = counts.get(num, 0) + 1

#         return sum(num for num in counts if counts[num] == 1)