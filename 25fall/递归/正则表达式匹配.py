def is_match(s: str, p: str) -> bool: 
    # bool声明此函数返回值为布尔值

    # 基本情况：如果模式p为空，只有当字符串s也为空时才完全匹配。
    # 这一步是终止条件（靠切片不断缩短子字符串长度）
    if not p:
        return not s
    
    # 检查第一个字符是否匹配，bool(s)确保s不为空，并储存一个逻辑判断式
    first_match = bool(s) and (s[0] == p[0] or p[0] == '.')
    
    # 如果模式长度至少为2且第二个字符是'*'
    if len(p) >= 2 and p[1] == '*':
        # 两种情况：
        # 1. '*'匹配0个前面的字符，直接跳过'*'和它前面的字符
        # 2. '*'匹配1个或多个前面的字符（需要第一个字符匹配），继续用相同模式匹配s的剩余部分
        return (is_match(s, p[2:]) or 
                (first_match and is_match(s[1:], p)))
    else:
        # 没有'*'的情况，正常匹配下一个字符
        return first_match and is_match(s[1:], p[1:])

# 当切片起始超出字符串长度时，返回空字符串
# 测试示例
print(is_match("aa", "a"))      # False
print(is_match("aa", "a*"))     # True
print(is_match("ab", ".*"))     # True
print(is_match("aab", "c*a*b")) # True
print(is_match("mississippi", "mis*is*p*.")) # False
