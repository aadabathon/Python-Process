#Simple Binary Search of the space implementation, O(logn(n))

class Solution(object):
    def firstBadVersion(self, n):
        def firstBadVersion(n):
            left = 1
            right = n

            while left < right:
                mid = left + (right - left) // 2
                if isBadVersion(mid):
                    right = mid 
                else:
                    left = mid + 1  
            return left 


        