def get_suffix_table(pattern):
    m = len(pattern)
    suffix = [0] * m
    suffix[m - 1] = m
    g = m - 1
    f = m - 1
    for i in range(m - 2, -1, -1):
        if i > g and suffix[i + m - 1 - f] < i - g:
            suffix[i] = suffix[i + m - 1 - f]
        else:
            if i < g:
                g = i
            f = i
            while g >= 0 and pattern[g] == pattern[g + m - 1 - f]:
                g -= 1
            suffix[i] = f - g
    return suffix


def get_good_suffix_table(pattern):
    m = len(pattern)
    suffix = get_suffix_table(pattern)
    good_suffix = [m] * m

    j = 0
    for i in range(m - 1, -1, -1):
        if suffix[i] == i + 1:
            while j < m - 1 - i:
                if good_suffix[j] == m:
                    good_suffix[j] = m - 1 - i
                j += 1

    for i in range(m - 1):
        good_suffix[m - 1 - suffix[i]] = m - 1 - i

    return good_suffix


def boyer_moore_search(text, pattern):
    n, m = len(text), len(pattern)
    if m == 0:
        return []

    good_suffix = get_good_suffix_table(pattern)
    indices = []
    s = 0

    while s <= n - m:
        j = m - 1

        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1

        if j < 0:
            indices.append(s)
            s += good_suffix[0]
        else:
            s += good_suffix[j]

    return indices

# T(n): Best: O(n/m); Worst: O(m*n)
