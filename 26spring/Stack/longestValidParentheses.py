def longestValidParentheses(s: str) -> int:
    stack = [-1]  # 初始参照点
    max_len = 0
    
    for end, char in enumerate(s):
        if char == '(':
            stack.append(end)
        else:
            stack.pop()
            if not stack:
                # 栈空了，说明这个 ')' 是多余的，把它设为新的参照起始点
                stack.append(end)
            else:
                # 计算当前有效括号的长度
                max_len = max(max_len, end - stack[-1])
                
    return max_len