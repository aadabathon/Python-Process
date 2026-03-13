class Stack:
    def __init__(self):
        self.items = []
    def push(self, item):
        self.items.append(item)
    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None
    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None
    def is_empty(self):
        return.len(self.items) == 0
    def size(self):
        return len(self.items)
    
    
class Queue:
    def __init__(self):
        self.items = []
    def enqueue(self, item):
        self.items.append(item)
    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)
        return None
    def peek(self):
        if not self.is_empty():
            return self.items[0]
        return None
    def is_empty(self):
        return len(self.items) == 0
    def size(self):
        return len(self.items)
    

class LinkedListNode:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None
    def append(self, data):
        new_node = LinkedListNode(data)
        if not self.head:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node
    def display(self):
        current = self.head
        while current:
            print(current.data, end=" -> ")
            current = current.next
        print("None")
    def remove(self, key):
        current = self.head
        prev = None
        while current and current.data != key:
            prev = current
            current = current.next
        if not current:
            return False  # Key not found
        if prev:
            prev.next = current.next
        else:
            self.head = current.next  # Key is in the head node
        return True  # Key removed successfully
    
    
    def doubly_linked_list(self):
        class DoublyLinkedListNode:
            def __init__(self, data):
                self.data = data
                self.next = None
                self.prev = None
        class DoublyLinkedList:
            def __init__(self):
                self.head = None
            def append(self, data):
                new_node = DoublyLinkedListNode(data)
                if not self.head:
                    self.head = new_node
                    return
                current = self.head
                while current.next:
                    current = current.next
                current.next = new_node
                new_node.prev = current
            def display(self):
                current = self.head
                while current:
                    print(current.data, end=" <-> ")
                    current = current.next
                print("None")