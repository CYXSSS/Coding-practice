class stack():
    def __init__(self, size):
        self.size = size
        self.stack = [None] * size
        self.top = -1
    def isEmpty(self):
        return self.top == -1
    def push(self, val):
        if self.top == self.size - 1:
            print("Stack is full")
        else:
            self.top += 1
            self.stack[self.top] = val
    def pop(self):
        if self.isEmpty():
            print("Stack is empty")
        else:
            val = self.stack[self.top]
            self.top -= 1
            return val
    def peek(self):
        if self.isEmpty():
            print("Stack is empty")
        else:
            return self.stack[self.top]
