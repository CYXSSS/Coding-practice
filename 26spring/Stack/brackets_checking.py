def brackets_checking(string):
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    for char in string:
        if char in mapping.values():
            stack.append(char)
        elif char in mapping.keys():
            if not stack or stack[-1] != mapping[char]:
                return False
            stack.pop()
    return not stack