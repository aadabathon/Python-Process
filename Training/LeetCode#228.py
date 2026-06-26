class Solution(object):
    def summaryRanges(self, nums):
        output_list = []    
        if (len(nums) < 2):
            if len(nums) == 1:
                output_list.append(str(nums[0]))
                return output_list
            else:
                return output_list
        elif (len(nums) == 2):
            if nums[0] == nums[1] - 1:
                output_list.append(str(nums[0]) + "->" + str(nums[1]))
            else:
                output_list.append(str(nums[0]))
                output_list.append(str(nums[1]))
            return output_list
        
        start = nums[0]
        for i in range(len(nums)):
            if not (nums[i + 1] == nums[i] + 1):
                if (nums[i] == start):
                    output_list.append(str(nums[i]))
                else:
                    output_list.append(str(start) + "->" + str(nums[i]))
                start = nums[i + 1]
            if (i+2 == len(nums)):
                if nums[i+1] == nums[i] + 1:
                    output_list.append(str(start) + "->" + str(nums[i+1]))
                else:
                    output_list.append(str(nums[i+1]))
                break
        return output_list