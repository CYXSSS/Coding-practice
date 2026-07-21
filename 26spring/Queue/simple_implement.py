class queue():
    def __init__(self, size):
        self.size = size
        self.queue = [None] * size
        self.head = 0
        self.tail = 0
    def is_empty(self):
        return self.head == self.tail
    def enqueue(self, val):
        if (self.tail + 1) % self.size == self.head:
            print("queue is full")
            return
        else:
            self.queue[self.tail] = val
            self.tail = (self.tail + 1) % self.size
    def dequeue(self):
        if self.is_empty():
            print("queue is empty")
            return
        else:
            self.queue[self.head] = None
            self.head = (self.head + 1) % self.size
    def peek(self):
        if self.is_empty():
            print("queue is empty")
            return
        else:
            return self.queue[self.head]

