
class Solution(object):
    def sizeUpTo(self, input_list, value):
        count = 0

        for x in input_list:
            if x < value:
                count += 1

        return count

    def distanceList(self, input_list, val):
        distances = set()
        lines = [1] + input_list + [val]
        lines.sort()
        for i in range(len(lines)):
            for j in range(i + 1, len(lines)):
                distances.add(lines[j] - lines[i])

        return distances

    def maximizeSquareArea(self, m, n, hFences, vFences):
        MOD = 10**9 + 7

        hDistance = self.distanceList(hFences, m)
        vDistance = self.distanceList(vFences, n)

        common = hDistance & vDistance

        if not common:
            return -1

        side = max(common)
        return (side * side) % MOD

        #idk how tf to solve this
        #for m == n, there is a square if theres a fence at x = (m>n) ? m : n
        #in any case, the best way to solve this is to find a greatest common
        #element between the two distance sets.

    """
    (1,1)-------(m-1)-----
    |
    |
    |
    |
    |
    (n-1)
    |
    |
    |
    |                 (a_m, a_n)
    """
