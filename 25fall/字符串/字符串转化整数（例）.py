def myAtoi(s: str) -> int:
    # 步骤1：去除前导空格
    s = s.lstrip()
    if not s:  # 空字符串直接返回0
        return 0
    
    # 步骤2：处理符号
    sign = 1
    index = 0
    if s[0] == '+':
        index += 1
    elif s[0] == '-':
        sign = -1
        index += 1
    
    # 步骤3：提取数字并转换
    result = 0
    max_int = 2 **31 - 1
    min_int = - (2** 31)
    
    while index < len(s) and s[index].isdigit():
        digit = int(s[index])
        # 检查是否溢出（提前判断，避免计算结果超出范围）
        # 这一步是（result = result * 10 + digit < max_int 的变式）
        if result > (max_int - digit) // 10:
            return max_int if sign == 1 else min_int
        # 直接累积数值而非使用字符串拼接
        result = result * 10 + digit
        index += 1
    
    # 步骤4：应用符号并返回
    return sign * result