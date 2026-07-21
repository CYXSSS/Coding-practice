def get_lps(pattern):
    m = len(pattern)
    lps = [0] * m
    length = 0  # 前一个最长相等前后缀的长度
    i = 1
    
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1] # 回退寻找次长前后缀
            else:
                lps[i] = 0
                i += 1
    return lps
# 生成 LPS 数组的最好、最坏时间复杂度为 O(m)

def kmp_search(text, pattern):
    n, m = len(text), len(pattern)
    if m == 0: return []
    
    lps = get_lps(pattern)
    i = j = 0 
    indices = []
    
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
            
        if j == m:
            indices.append(i - j)
            j = lps[j - 1] # 匹配成功后，继续寻找下一个匹配
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1] # 发生失配，利用 LPS 数组跳跃
            else:
                i += 1
                
    return indices
# 匹配阶段时间复杂度为 O(n)

# KMP 算法的总时间复杂度为 O(n+m)