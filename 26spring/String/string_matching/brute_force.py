def naive_search(text, pattern):
    n, m = len(text), len(pattern)
    if m == 0: return []
    
    indices = []
    # 遍历主串，终点是 n - m
    for i in range(n - m + 1):
        j = 0
        # 逐个字符比对
        while j < m and text[i + j] == pattern[j]:
            j += 1
        
        # 如果 j 走到了模式串的末尾，说明完全匹配
        if j == m:
            indices.append(i)
            
    return indices

# 测试
txt = "ABABDABACDABABCABAB"
pat = "ABABCABAB"
print(f"Naive 匹配结果: {naive_search(txt, pat)}")

# T(n): Best: O(n); Worst: O(m*n)