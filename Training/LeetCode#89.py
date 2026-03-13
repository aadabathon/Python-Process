#Bitwise operations
#i ^ (i >> 1)
#so for i in range(0, 2**n) add 
#could be far more efficient using numerical bit operations shown below:
#The pattern is flipping the current string and adding the current bit value
"""
def grayCode(self, n):
        res = [0]
        bit = 1
        while n > 0:
            layer = res[::-1]
            for i in layer:
                res.append(i+bit)
            bit += bit
            n -= 1
        return res
"""
class Solution(object):
    def grayCode(self, n):
        def gray(i):
            return i ^ (i>>1)
        GrayString = [0] * 2**n
        for j in range(1, 2**n):
            GrayString[j] = (gray(j))
        return GrayString