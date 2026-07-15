
# class Solution(object):
#     def sampleStats(self, count):
#         """
#         Treating count as a raw dataset, not a histogram.

#         :type count: List[int]
#         :rtype: List[float]
#         """
#         if not count:
#             return None

#         min_val = float("inf")
#         max_val = float("-inf")

#         for num in count:
#             if num < min_val:
#                 min_val = num

#             if num > max_val:
#                 max_val = num

#         total = 0
#         for num in count:
#             total += num

#         mean = float(total) / len(count)

#         sorted_count = sorted(count)

#         n = len(sorted_count)
#         if n % 2 == 0:
#             median = (sorted_count[n // 2] + sorted_count[n // 2 - 1]) / 2.0
#         else:
#             median = sorted_count[n // 2]

#         frequencies = {}

#         for num in count:
#             if num not in frequencies:
#                 frequencies[num] = 1
#             else:
#                 frequencies[num] += 1

#         mode = None
#         highest_frequency = 0

#         for num in frequencies:
#             if frequencies[num] > highest_frequency:
#                 highest_frequency = frequencies[num]
#                 mode = num

#         return [float(min_val), float(max_val), mean, median, float(mode)]



# class Solution(object):
#     def sampleStats(self, count):
#         """
#         :type count: List[int]
#         :rtype: List[float]
#         """
#         max = 0

#         for i in count:
#             if i > max:
#                 max = i:
        
#         min = float ("inf")

#         for i in count:
#             if i < min:
#                 min = i

#         mean = 0
#         for i in count
#             mean += i
#         mean = mean/len(count)

#         sorted_count = count.sort()
#         median = 0
#         if not count:
#             return None
#         if len(count)%2 == 0:
#             median = (sorted_count[len(count)/2] + sorted_count[len(count)/2 - 1])/2
#         else:
#             median = sorted_count[len(count)/2 -1]

#         mode = 0
#         dict = {}

#         for i in count:
#             dict(i) += 1

#         count = 0
#         for i in dict:
#             if dict(i) > count:
#                 count = dict(i)
#                 mode = 
#         return [min, max, mean, median, mode]

