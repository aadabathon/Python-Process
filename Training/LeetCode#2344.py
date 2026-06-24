class Solution(object):

    def GCD_nums(self, a, b):
        if b == 0:
            return a
        return self.GCD_nums(b, a % b)

    def GCD_list(self, input_list):
        gcd = input_list[0]

        for i in input_list[1:]:
            gcd = self.GCD_nums(gcd, i)

        return gcd

    def minOperations(self, nums, numsDivide):
        gcd = self.GCD_list(numsDivide)
        sorted_nums = sorted(nums)

        for deletions, num in enumerate(sorted_nums):
            if gcd % num == 0:
                return deletions

        return -1


# Deprecated helper method:
#
# def smallest(self, input_list):
#     smallest = float("Inf")
#
#     for i in input_list:
#         if i < smallest:
#             smallest = i
#
#     return smallest


# Deprecated helper method:
#
# def removeAll(self, toRemove, remove_list):
#     removed = 0
#
#     for i in range(len(remove_list)):
#         if remove_list[i - removed] == toRemove:
#             remove_list.remove(toRemove)
#             removed += 1
#
#     return remove_list


# Deprecated minOperations method using repeated smallest-removal:
#
# def minOperations(self, nums, numsDivide):
#     gcd = self.GCD_list(numsDivide)
#     smallest = self.smallest(nums)
#     min_deletions = 0
#
#     while gcd % smallest != 0:
#         old_len = len(nums)
#         nums = self.removeAll(smallest, nums)
#         min_deletions += old_len - len(nums)
#
#         if not nums:
#             break
#
#         smallest = self.smallest(nums)
#
#     if not nums:
#         return -1
#
#     return min_deletions


# Deprecated brute-force minOperations method:
#
# def minOperations(self, nums, numsDivide):
#     divides = False
#     over = False
#     smallest = self.smallest(nums)
#     min_deletions = float("Inf")
#     hit_count = 0
#     del_count = 0
#
#     while not (over or divides):
#         for j in range(len(numsDivide)):
#             if numsDivide[j] % smallest == 0:
#                 hit_count += 1
#
#                 if len(numsDivide) == hit_count:
#                     divides = True
#                     min_deletions = del_count
#             else:
#                 break
#
#         if not divides:
#             old_len = len(nums)
#             nums = self.removeAll(smallest, nums)
#             del_count += old_len - len(nums)
#             smallest = self.smallest(nums)
#             over = not nums
#
#     if over:
#         return -1
#     elif divides:
#         return min_deletions
#     else:
#         print("what the heck")
