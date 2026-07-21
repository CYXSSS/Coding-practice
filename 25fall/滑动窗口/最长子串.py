def length_of_longest_substring(s: str) -> int:
    # 用于存储字符最后出现的位置
    char_index = {}
    # 最长子串长度，初始为0
    max_length = 0
    # 滑动窗口的起始位置
    start = 0
    
    # 遍历字符串，end为滑动窗口的结束位置（enumerate将检索值，键。位置是反的）
    for end, char in enumerate(s):
        # 如果字符已存在于字典中，并且其位置在当前窗口内
        if char in char_index and char_index[char] >= start:
            # 移动窗口起始位置到重复字符的下一个位置
            start = char_index[char] + 1
        
        # 更新字符最后出现的位置
        char_index[char] = end
        # 计算当前窗口长度，并更新最大长度（重点掌握：记录值的写法）
        current_length = end - start + 1
        if current_length > max_length:
            max_length = current_length
    
    return max_length

# 接收用户输入并计算结果
if __name__ == "__main__":
    # 获取用户输入的字符串
    user_input = input("请输入一个字符串：")
    
    # 计算最长无重复子串的长度
    result = length_of_longest_substring(user_input)
    
    # 输出结果
    print(f"该字符串中不含重复字符的最长子串长度为：{result}")
