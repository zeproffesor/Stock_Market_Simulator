from collections import deque

class Queue(deque):

    def __init__(self):
        self.deleted = set()
    
    def push(self, x):
        self.append(x)

    def pop(self):
        while self.size() and self[0] in self.deleted:
            self.deleted.remove(self[0])
            self.popleft()
        return self.popleft() if self.size() else None

    def front(self):
        while self.size() and self[0] in self.deleted:
            self.deleted.remove(self[0])
            self.popleft()
        return self[0] if self.size() else None
    
    def remove(self, x):
        self.deleted.add(x)

    def size(self):
        return len(self)-len(self.deleted)