def get_bad_char_table(pattern):
    m = len(pattern)
    bad_chars = {}
    for i in range(m):
        bad_chars[pattern[i]] = i
    return bad_chars

def boyer_moore_search(text, pattern):
    n, m = len(text), len(pattern)
    if m == 0: return []
    
    bad_chars = get_bad_char_table(pattern)
    indices = []
    s = 0
    
    while s <= n - m:
        j = m - 1
        
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
            
        if j < 0:
            indices.append(s)
            if s + m < n:
                next_char = text[s + m]
                s += m - bad_chars.get(next_char, -1)
            else:
                s += 1
        else:
            bad_char = text[s + j]
            bad_char_idx = bad_chars.get(bad_char, -1)
            s += max(1, j - bad_char_idx)
            
    return indices

# T(n): Best: O(n/m); Worst: O(m*n)
