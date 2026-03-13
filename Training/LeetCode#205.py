#simple Dict Mapping problem.
class solution(object):
        def isIsomorphic(self, s, t):
                if len(s) != len(t):
                        return False
                TonS = {}
                SonT = {}
                for char_s, char_t in zip(s,t):
                        if char_s in SonT:
                                if SonT[char_s] != char_t:
                                        return False
                        else:
                                SonT[char_s] = char_t
                        if char_t in TonS:
                                if TonS[char_t] != char_s:
                                        return False
                        else: 
                                TonS[char_t] = char_s

                return True