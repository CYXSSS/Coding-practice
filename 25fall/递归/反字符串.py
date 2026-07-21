def reverse_string(s):
    if len(s) <= 1:
        return s
    n = len(s)
    return s[n-1] + reverse_string(s[0:n-1])
# 测试代码
print(reverse_string("Hello, World!"))
print(reverse_string("abcdefg"))   
