class HappyNum:
    def isHappy(self, n):
        seen= []
        while n!=1:
            if n in seen:
                return false:
            seen.append(n)
            n = sum(num ** 2 for num in str(n))
        return True
    
        