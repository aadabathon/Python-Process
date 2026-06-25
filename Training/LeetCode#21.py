# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution(object):
    def mergeTwoLists(self, list1, list2):
        if list1 is None:
            return list2
        elif list2 is None:
            return list1
        elif (list1.val >= list2.val):
            head = list2
            list2 = list2.next
        else:
            head = list1
            list1 = list1.next
        curr = head
        while (list1 or list2):
            if list1 is None:
                curr.next = list2
                break
            elif list2 is None:
                curr.next = list1
                break
            elif (list1.val >= list2.val):
                curr.next = list2
                curr = curr.next
                list2 = list2.next
            elif (list1.val < list2.val):
                curr.next = list1
                curr = curr.next
                list1 = list1.next

        return head