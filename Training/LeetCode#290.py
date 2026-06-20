class Solution(object):
    def wordPattern(self, pattern, s):

        def cleanList(input_iterable):
            word_list = []
            string = ""
            for char in input_iterable:
                if char != " ":
                    string = string + char
                else:
                    word_list.append(string)
                    string = ""
            word_list.append(string)
            return word_list

        def isSeen(input_iterable):
            hash_table = {}
            n = 0
            output = []
            for element in input_iterable:
                if element not in hash_table:
                    n += 1
                    hash_table[element] = n
            for element in input_iterable:
                output.append(hash_table[element])
            return output

        cleanList = cleanList(s)
        return (isSeen(cleanList) == isSeen(pattern))


        
